from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field

from ...schemas import WebsocketResponse


class AsyncWebsocketCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI websocket connection."""

    websocket: WebSocket = Field(...)
    response: WebsocketResponse = Field(...)

    class Config:
        arbitrary_types_allowed = True

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True


class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.websocket.send_json({**self.response.dict(), **{"message": token}})
