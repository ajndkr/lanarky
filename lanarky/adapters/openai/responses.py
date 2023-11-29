from typing import Any

from fastapi import status
from starlette.types import Send

from lanarky.adapters.openai.resources import Message
from lanarky.events import Events, ServerSentEvent, ensure_bytes
from lanarky.logging import logger
from lanarky.responses import HTTPStatusDetail
from lanarky.responses import StreamingResponse as _StreamingResponse

from .resources import OpenAIResource


class StreamingResponse(_StreamingResponse):
    """StreamingResponse class for OpenAI resources."""

    def __init__(
        self,
        resource: OpenAIResource,
        messages: list[Message],
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> None:
        """Constructor method.

        Args:
            resource: An OpenAIResource instance.
            messages: A list of `Message` instances.
            *args: Positional arguments to pass to the parent constructor.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """
        super().__init__(*args, **kwargs)

        self.resource = resource
        self.messages = messages

    async def stream_response(self, send: Send) -> None:
        """Stream chat completions.

        If an exception occurs while iterating over the OpenAI resource, an
        internal server error is sent to the client.

        Args:
            send: The ASGI send callable.
        """
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        try:
            async for chunk in self.resource.stream_response(self.messages):
                event_body = ServerSentEvent(
                    data=chunk,
                    event=Events.COMPLETION,
                )
                await send(
                    {
                        "type": "http.response.body",
                        "body": ensure_bytes(event_body, None),
                        "more_body": True,
                    }
                )
        except Exception as e:
            logger.error(f"openai error: {e}")
            error_event_body = ServerSentEvent(
                data=dict(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=HTTPStatusDetail.INTERNAL_SERVER_ERROR,
                ),
                event=Events.ERROR,
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": ensure_bytes(error_event_body, None),
                    "more_body": True,
                }
            )

        await send({"type": "http.response.body", "body": b"", "more_body": False})
