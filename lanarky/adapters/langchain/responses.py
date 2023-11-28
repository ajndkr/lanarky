from typing import Any

from fastapi import status
from langchain.chains.base import Chain
from starlette.types import Send

from lanarky.events import Events, ServerSentEvent, ensure_bytes
from lanarky.logging import logger
from lanarky.responses import HTTPStatusDetail
from lanarky.responses import StreamingResponse as _StreamingResponse


class StreamingResponse(_StreamingResponse):
    """StreamingResponse class for LangChain resources."""

    def __init__(
        self,
        chain: Chain,
        config: dict[str, Any],
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> None:
        """Constructor method.

        Args:
            chain: A LangChain instance.
            config: A config dict.
            *args: Positional arguments to pass to the parent constructor.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """
        super().__init__(*args, **kwargs)

        self.chain = chain
        self.config = config

    async def stream_response(self, send: Send) -> None:
        """Stream LangChain outputs.

        If an exception occurs while iterating over the LangChain, an
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

        if "callbacks" in self.config:
            for callback in self.config["callbacks"]:
                if hasattr(callback, "send"):
                    callback.send = send

        try:
            # TODO: migrate to `.ainvoke` when adding support
            # for LCEL
            outputs = await self.chain.acall(**self.config)
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
