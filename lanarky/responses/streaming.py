"""
Credits:

* `gist@ninely <https://gist.github.com/ninely/88485b2e265d852d3feb8bd115065b1a>`_
* `langchain@#1705 <https://github.com/hwchase17/langchain/discussions/1706>`_
"""
from typing import Any, Awaitable, Callable, Optional, Union

from fastapi.responses import StreamingResponse as _StreamingResponse
from langchain.chains.base import Chain
from starlette.background import BackgroundTask
from starlette.types import Send

from lanarky.callbacks import get_streaming_callback, get_streaming_json_callback


class StreamingResponse(_StreamingResponse):
    """StreamingResponse class wrapper for langchain chains."""

    def __init__(
        self,
        chain_executor: Callable[[Send], Awaitable[Any]],
        background: Optional[BackgroundTask] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(content=iter(()), background=background, **kwargs)

        self.chain_executor = chain_executor

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        try:
            outputs = await self.chain_executor(send)
            if self.background is not None:
                self.background.kwargs["outputs"] = outputs
        except Exception as e:
            if self.background is not None:
                self.background.kwargs["outputs"] = str(e)
            await send(
                {
                    "type": "http.response.body",
                    "body": str(e).encode(self.charset),
                    "more_body": False,
                }
            )
            return

        await send({"type": "http.response.body", "body": b"", "more_body": False})

    @staticmethod
    def _create_chain_executor(
        chain: Chain,
        inputs: Union[dict[str, Any], Any],
        as_json: bool = False,
        **callback_kwargs,
    ) -> Callable[[Send], Awaitable[Any]]:
        get_callback_fn = (
            get_streaming_json_callback if as_json else get_streaming_callback
        )

        async def wrapper(send: Send):
            return await chain.acall(
                inputs=inputs,
                callbacks=[get_callback_fn(chain, send=send, **callback_kwargs)],
            )

        return wrapper

    @classmethod
    def from_chain(
        cls,
        chain: Chain,
        inputs: Union[dict[str, Any], Any],
        as_json: bool = False,
        background: Optional[BackgroundTask] = None,
        callback_kwargs: dict[str, Any] = {},
        **kwargs: Any,
    ) -> "StreamingResponse":
        chain_executor = cls._create_chain_executor(
            chain, inputs, as_json, **callback_kwargs
        )

        return cls(
            chain_executor=chain_executor,
            background=background,
            **kwargs,
        )
