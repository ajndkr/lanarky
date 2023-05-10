from langchain.chains.base import Chain

from .base import AsyncStreamingResponseCallback, AsyncWebsocketCallback
from .llm import (
    AsyncConversationChainStreamingCallback,
    AsyncConversationChainWebsocketCallback,
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainWebsocketCallback,
)
from .qa_with_sources import (
    AsyncQAWithSourcesChainStreamingCallback,
    AsyncQAWithSourcesChainWebsocketCallback,
    AsyncRetrievalQAWithSourcesChainStreamingCallback,
    AsyncRetrievalQAWithSourcesChainWebsocketCallback,
    AsyncVectorDBQAWithSourcesChainStreamingCallback,
    AsyncVectorDBQAWithSourcesChainWebsocketCallback,
)
from .retrieval_qa import (
    AsyncRetrievalQAStreamingCallback,
    AsyncRetrievalQAWebsocketCallback,
    AsyncVectorDBQAStreamingCallback,
    AsyncVectorDBQAWebsocketCallback,
)

# TODO: update logic to use decorate to
# register callbacks
STREAMING_CALLBACKS_REGISTRY = {
    AsyncLLMChainStreamingCallback.chain_type: AsyncLLMChainStreamingCallback,
    AsyncConversationChainStreamingCallback.chain_type: AsyncConversationChainStreamingCallback,
    AsyncRetrievalQAStreamingCallback.chain_type: AsyncRetrievalQAStreamingCallback,
    AsyncVectorDBQAStreamingCallback.chain_type: AsyncVectorDBQAStreamingCallback,
    AsyncQAWithSourcesChainStreamingCallback.chain_type: AsyncQAWithSourcesChainStreamingCallback,
    AsyncRetrievalQAWithSourcesChainStreamingCallback.chain_type: AsyncRetrievalQAWithSourcesChainStreamingCallback,
    AsyncVectorDBQAWithSourcesChainStreamingCallback.chain_type: AsyncVectorDBQAWithSourcesChainStreamingCallback,
}

WEBSOCKET_CALLBACKS_REGISTRY = {
    AsyncLLMChainWebsocketCallback.chain_type: AsyncLLMChainWebsocketCallback,
    AsyncConversationChainWebsocketCallback.chain_type: AsyncConversationChainWebsocketCallback,
    AsyncRetrievalQAWebsocketCallback.chain_type: AsyncRetrievalQAWebsocketCallback,
    AsyncVectorDBQAWebsocketCallback.chain_type: AsyncVectorDBQAWebsocketCallback,
    AsyncQAWithSourcesChainWebsocketCallback.chain_type: AsyncQAWithSourcesChainWebsocketCallback,
    AsyncRetrievalQAWithSourcesChainWebsocketCallback.chain_type: AsyncRetrievalQAWithSourcesChainWebsocketCallback,
    AsyncVectorDBQAWithSourcesChainWebsocketCallback.chain_type: AsyncVectorDBQAWithSourcesChainWebsocketCallback,
}


def get_streaming_callback(
    chain: Chain, *args, **kwargs
) -> AsyncStreamingResponseCallback:
    """Get the streaming callback for the given chain type."""
    chain_type = chain.__class__.__name__
    return STREAMING_CALLBACKS_REGISTRY[chain_type](*args, **kwargs)


def get_websocket_callback(chain: Chain, *args, **kwargs) -> AsyncWebsocketCallback:
    """Get the websocket callback for the given chain type."""
    chain_type = chain.__class__.__name__
    return WEBSOCKET_CALLBACKS_REGISTRY[chain_type](*args, **kwargs)
