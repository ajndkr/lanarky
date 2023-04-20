from typing import Any

from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field
from starlette.types import Send


class AsyncFastApiStreamingCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI StreamingResponse."""

    send: Send = Field(...)

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.send(token)
