from typing import Any

from lanarky.register import (
    register_streaming_callback,
    register_streaming_json_callback,
    register_websocket_callback,
)
from lanarky.schemas import AnswerStreamingJSONResponse, StreamingJSONResponse

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
        if self.llm_cache_used:  # cache missed (or was never enabled) if we are here
            self.llm_cache_used = False
        message = self._construct_message(token)
        await self.send(message)

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        # If the cache was used, we need to send the final answer.
        if self.llm_cache_used and self.output_key in outputs:
            message = self._construct_message(outputs[self.output_key])
            await self.send(message)


@register_websocket_callback(SUPPORTED_CHAINS)
class AsyncLLMChainWebsocketCallback(AsyncWebsocketCallback):
    """AsyncWebsocketCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if self.llm_cache_used:  # cache missed (or was never enabled) if we are here
            self.llm_cache_used = False
        message = self._construct_message(token)
        await self.websocket.send_json(message)

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        # If the cache was used, we need to send the final answer.
        if self.llm_cache_used and self.output_key in outputs:
            message = self._construct_message(outputs[self.output_key])
            await self.websocket.send_json(message)


@register_streaming_json_callback(SUPPORTED_CHAINS)
class AsyncLLMChainStreamingJSONCallback(AsyncStreamingJSONResponseCallback):
    """AsyncStreamingJSONResponseCallback handler for LLMChain."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if self.llm_cache_used:  # cache missed (or was never enabled) if we are here
            self.llm_cache_used = False
        message = self._construct_message(StreamingJSONResponse(token=token))
        await self.send(message)

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        # If the cache was used, we need to send the final answer.
        if self.llm_cache_used and self.output_key in outputs:
            message = self._construct_message(
                AnswerStreamingJSONResponse(answer=outputs[self.output_key])
            )
            await self.send(message)
