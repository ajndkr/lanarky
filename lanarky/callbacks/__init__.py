from langchain.chains.base import Chain

from lanarky.register import STREAMING_CALLBACKS, WEBSOCKET_CALLBACKS

from .agents import AsyncAgentsStreamingCallback, AsyncAgentsWebsocketCallback
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
    "AsyncAgentsStreamingCallback",
    "AsyncAgentsWebsocketCallback",
]

ERROR_MESSAGE = """Error! Chain type '{chain_type}' is not currently supported by '{callable_name}'."""


def get_streaming_callback(
    chain: Chain, *args, **kwargs
) -> AsyncStreamingResponseCallback:
    """Get the streaming callback for the given chain type."""
    chain_type = chain.__class__.__name__
    try:
        callback = STREAMING_CALLBACKS[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type, callable_name="AsyncStreamingResponseCallback"
            )
        )


def get_websocket_callback(chain: Chain, *args, **kwargs) -> AsyncWebsocketCallback:
    """Get the websocket callback for the given chain type."""
    chain_type = chain.__class__.__name__
    try:
        callback = WEBSOCKET_CALLBACKS[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type, callable_name="AsyncWebsocketCallback"
            )
        )
