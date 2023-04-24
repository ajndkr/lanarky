from functools import partial
from typing import Any, Dict, Union

from fastapi.responses import StreamingResponse
from langchain.chains.base import Chain
from starlette.types import Send


class BaseLangchainStreamingResponse(StreamingResponse):
    """Base StreamingResponse class wrapper for langchain chains."""

    def __init__(
        self,
        chain: Chain,
        inputs: Union[Dict[str, Any], Any],
        **kwargs: Any,
    ) -> None:
        super().__init__(content=iter(()), **kwargs)

        self.chain_wrapper_fn = self.chain_wrapper_fn(chain, inputs)

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

    @staticmethod
    def chain_wrapper_fn(chain: Chain, inputs: Union[Dict[str, Any], Any]):
        raise NotImplementedError
