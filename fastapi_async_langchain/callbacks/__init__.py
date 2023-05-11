from langchain.chains.base import Chain

from fastapi_async_langchain.register import STREAMING_CALLBACKS, WEBSOCKET_CALLBACKS

from .base import AsyncStreamingResponseCallback, AsyncWebsocketCallback
from .llm import (
    AsyncConversationChainStreamingCallback,
    AsyncConversationChainWebsocketCallback,
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainWebsocketCallback,
)
from .qa_with_sources import (
    AsyncConversationalRetrievalChainStreamingCallback,
    AsyncConversationalRetrievalChainWebsocketCallback,
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

__all__ = [
    "AsyncLLMChainStreamingCallback",
    "AsyncLLMChainWebsocketCallback",
    "AsyncConversationChainStreamingCallback",
    "AsyncConversationChainWebsocketCallback",
    "AsyncRetrievalQAStreamingCallback",
    "AsyncRetrievalQAWebsocketCallback",
    "AsyncVectorDBQAStreamingCallback",
    "AsyncVectorDBQAWebsocketCallback",
    "AsyncQAWithSourcesChainStreamingCallback",
    "AsyncQAWithSourcesChainWebsocketCallback",
    "AsyncRetrievalQAWithSourcesChainStreamingCallback",
    "AsyncRetrievalQAWithSourcesChainWebsocketCallback",
    "AsyncVectorDBQAWithSourcesChainStreamingCallback",
    "AsyncVectorDBQAWithSourcesChainWebsocketCallback",
    "AsyncConversationalRetrievalChainStreamingCallback",
    "AsyncConversationalRetrievalChainWebsocketCallback",
]


def get_streaming_callback(
    chain: Chain, *args, **kwargs
) -> AsyncStreamingResponseCallback:
    """Get the streaming callback for the given chain type."""
    chain_type = chain.__class__.__name__
    return STREAMING_CALLBACKS[chain_type](*args, **kwargs)


def get_websocket_callback(chain: Chain, *args, **kwargs) -> AsyncWebsocketCallback:
    """Get the websocket callback for the given chain type."""
    chain_type = chain.__class__.__name__
    return WEBSOCKET_CALLBACKS[chain_type](*args, **kwargs)
