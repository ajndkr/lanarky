from typing import Any

from fastapi import status
from langchain.chains.base import Chain
from sse_starlette.sse import ServerSentEvent
from starlette.types import Send

from lanarky.logging import logger
from lanarky.responses import Events, HTTPStatusDetail
from lanarky.responses import StreamingResponse as _StreamingResponse
from lanarky.responses import ensure_bytes


class StreamingResponse(_StreamingResponse):
    def __init__(
        self,
        chain: Chain,
        chain_config: dict[str, Any],
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.chain = chain
        self.chain_config = chain_config

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        if "callbacks" in self.chain_config:
            for callback in self.chain_config["callbacks"]:
                if hasattr(callback, "send"):
                    callback.send = send

        try:
            # TODO: migrate to `.ainvoke` when adding support
            # for LCEL
            outputs = await self.chain.acall(**self.chain_config)
            if self.background is not None:
                self.background.kwargs.update({"outputs": outputs})
        except Exception as e:
            logger.error(f"chain runtime error: {e}")
            if self.background is not None:
                self.background.kwargs.update({"outputs": {}, "error": e})
            chunk = ServerSentEvent(
                data=dict(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=HTTPStatusDetail.INTERNAL_SERVER_ERROR,
                ),
                event=Events.ERROR,
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": ensure_bytes(chunk, None),
                    "more_body": True,
                }
            )

        await send({"type": "http.response.body", "body": b"", "more_body": False})
