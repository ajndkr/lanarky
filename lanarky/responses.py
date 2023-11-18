from enum import Enum
from typing import Any

from fastapi import status
from sse_starlette.sse import EventSourceResponse, ServerSentEvent, ensure_bytes
from starlette.types import Send

from lanarky.logging import logger


class Events(str, Enum):
    ERROR = "error"


class HTTPStatusDetail(str, Enum):
    INTERNAL_SERVER_ERROR = "Internal Server Error"


class StreamingResponse(EventSourceResponse):
    """Base class for all streaming responses.

    ``StreamingResponse`` follows the EventSource protocol:
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events#interfaces
    """

    def __init__(
        self,
        content: Any = iter(()),
        *args,
        **kwargs,
    ) -> None:
        super().__init__(content=content, *args, **kwargs)

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        try:
            async for data in self.body_iterator:
                chunk = ensure_bytes(data, self.sep)
                logger.debug(f"chunk: {chunk.decode()}")
                await send(
                    {"type": "http.response.body", "body": chunk, "more_body": True}
                )
        except Exception as e:
            logger.error(f"body iterator error: {e}")
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
