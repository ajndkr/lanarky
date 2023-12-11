import asyncio
from functools import partial
from typing import Any

from fastapi import status
from langchain.chains.base import Chain
from starlette.types import Send

from lanarky.events import Events, ServerSentEvent, ensure_bytes
from lanarky.logging import logger
from lanarky.responses import HTTPStatusDetail
from lanarky.responses import StreamingResponse as _StreamingResponse
from lanarky.utils import StrEnum


class ChainRunMode(StrEnum):
    """Enum for LangChain run modes."""

    ASYNC = "async"
    SYNC = "sync"


class StreamingResponse(_StreamingResponse):
    """StreamingResponse class for LangChain resources."""

    def __init__(
        self,
        chain: Chain,
        config: dict[str, Any],
        run_mode: ChainRunMode = ChainRunMode.ASYNC,
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

        if run_mode not in list(ChainRunMode):
            raise ValueError(
                f"Invalid run mode '{run_mode}'. Must be one of {list(ChainRunMode)}"
            )

        self.run_mode = run_mode

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
            if self.run_mode == ChainRunMode.ASYNC:
                outputs = await self.chain.acall(**self.config)
            else:
                loop = asyncio.get_event_loop()
                outputs = await loop.run_in_executor(
                    None, partial(self.chain, **self.config)
                )
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
