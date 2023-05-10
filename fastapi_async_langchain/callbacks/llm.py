from typing import Any

from .base import AsyncStreamingResponseCallback, AsyncWebsocketCallback


class AsyncLLMChainStreamingCallback(AsyncStreamingResponseCallback):
    """AsyncStreamingResponseCallback handler for LLMChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "LLMChain"

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.send(token)


class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "LLMChain"

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.websocket.send_json({**self.response.dict(), **{"message": token}})


class AsyncConversationChainStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for ConversationChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "ConversationChain"


class AsyncConversationChainWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for ConversationChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "ConversationChain"
