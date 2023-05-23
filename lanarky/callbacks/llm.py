from typing import Any

from lanarky.register import (
    register_streaming_callback,
    register_streaming_json_callback,
    register_websocket_callback,
)
from lanarky.schemas import StreamingJSONResponse

from .base import (
    AsyncStreamingJSONResponseCallback,
    AsyncStreamingResponseCallback,
    AsyncWebsocketCallback,
)

SUPPORTED_CHAINS = ["LLMChain", "ConversationChain"]


@register_streaming_callback(SUPPORTED_CHAINS)
class AsyncLLMChainStreamingCallback(AsyncStreamingResponseCallback):
    """AsyncStreamingResponseCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(token)
        await self.send(message)


@register_websocket_callback(SUPPORTED_CHAINS)
class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(token)
        await self.websocket.send_json(message)


@register_streaming_json_callback(SUPPORTED_CHAINS)
class AsyncLLMChainStreamingJSONCallback(AsyncStreamingJSONResponseCallback):
    """AsyncStreamingJSONResponseCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(StreamingJSONResponse(token=token))
        await self.send(message)
