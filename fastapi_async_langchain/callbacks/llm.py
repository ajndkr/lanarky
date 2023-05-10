from typing import Any

from .base import AsyncStreamingResponseCallback, AsyncWebsocketCallback


class AsyncLLMChainStreamingCallback(AsyncStreamingResponseCallback):
    """AsyncStreamingResponseCallback handler for LLMChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "LLMChain"

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.send(token)


class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "LLMChain"

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.websocket.send_json({**self.response.dict(), **{"message": token}})


class AsyncConversationChainStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for ConversationChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "ConversationChain"


class AsyncConversationChainWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for ConversationChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "ConversationChain"
