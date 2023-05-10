"""
Credits:
- https://gist.github.com/ninely/88485b2e265d852d3feb8bd115065b1a
- https://github.com/hwchase17/langchain/discussions/1706
"""
from abc import abstractstaticmethod
from typing import Any, Awaitable, Callable, Dict, Optional, Union

from fastapi.responses import StreamingResponse
from langchain.chains.base import Chain
from starlette.background import BackgroundTask
from starlette.types import Send


class BaseLangchainStreamingResponse(StreamingResponse):
    """Base StreamingResponse class wrapper for langchain chains."""

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

        async def send_token(token: Union[str, bytes]):
            if not isinstance(token, bytes):
                token = token.encode(self.charset)
            await send({"type": "http.response.body", "body": token, "more_body": True})

        try:
            outputs = await self.chain_executor(send_token)
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

    @abstractstaticmethod
    def _create_chain_executor(
        chain: Chain, inputs: Union[Dict[str, Any], Any]
    ) -> Callable[[Send], Awaitable[Any]]:
        raise NotImplementedError

    @classmethod
    def from_chain(
        cls,
        chain: Chain,
        inputs: Union[Dict[str, Any], Any],
        background: Optional[BackgroundTask] = None,
        **kwargs: Any,
    ) -> "BaseLangchainStreamingResponse":
        chain_executor = cls._create_chain_executor(chain, inputs)

        return cls(
            chain_executor=chain_executor,
            background=background,
            **kwargs,
        )
