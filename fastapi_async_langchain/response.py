from functools import partial
from typing import Any, Dict, Union

from fastapi.responses import StreamingResponse
from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager
from starlette.types import Send

from .callback import AsyncFastApiStreamingCallback


class LangchainStreamingResponse(StreamingResponse):
    """StreamingResponse for langchain LLM chains."""

    def __init__(
        self,
        chain: LLMChain,
        inputs: Union[Dict[str, Any], Any],
        **kwargs: Any,
    ) -> None:
        super().__init__(content=iter(()), **kwargs)

        def chain_wrapper_fn(chain: LLMChain, inputs: Union[Dict[str, Any], Any]):
            async def wrapper(send: Send):
                if not isinstance(chain.llm.callback_manager, AsyncCallbackManager):
                    raise TypeError(
                        "llm.callback_manager must be an instance of AsyncCallbackManager"
                    )
                for handler in chain.llm.callback_manager.handlers:
                    if isinstance(handler, AsyncFastApiStreamingCallback):
                        chain.llm.callback_manager.remove_handler(handler)
                        break
                chain.llm.callback_manager.add_handler(
                    AsyncFastApiStreamingCallback(send=send)
                )
                return await chain.arun(inputs)

            return wrapper

        self.chain_wrapper_fn = chain_wrapper_fn(chain, inputs)

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
            outputs = await self.chain_wrapper_fn(send_token)
            if self.background is not None:
                self.background = partial(self.background, outputs)
        except Exception as e:
            await send(
                {
                    "type": "http.response.body",
                    "body": str(e).encode(self.charset),
                    "more_body": False,
                }
            )
            return

        await send({"type": "http.response.body", "body": b"", "more_body": False})
