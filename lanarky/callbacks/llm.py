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


@register_streaming_callback("LLMChain")
class AsyncLLMChainStreamingCallback(AsyncStreamingResponseCallback):
    """AsyncStreamingResponseCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(token)
        await self.send(message)


@register_websocket_callback("LLMChain")
class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(token)
        await self.websocket.send_json(message)


@register_streaming_json_callback("LLMChain")
class AsyncLLMChainStreamingJSONCallback(AsyncStreamingJSONResponseCallback):
    """AsyncStreamingJSONResponseCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        message = self._construct_message(StreamingJSONResponse(token=token))
        await self.send(message)


@register_streaming_callback("ConversationChain")
class AsyncConversationChainStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for ConversationChain."""

    pass


@register_websocket_callback("ConversationChain")
class AsyncConversationChainWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for ConversationChain."""

    pass


@register_streaming_json_callback("ConversationChain")
class AsyncConversationChainStreamingJSONCallback(AsyncLLMChainStreamingJSONCallback):
    """AsyncStreamingJSONResponseCallback handler for ConversationChain."""

    pass
