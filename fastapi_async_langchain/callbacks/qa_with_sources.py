from fastapi_async_langchain.register import (
    register_streaming_callback,
    register_websocket_callback,
)

from .retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)


@register_streaming_callback("BaseQAWithSources")
class AsyncBaseQAWithSourcesChainStreamingCallback(
    AsyncBaseRetrievalQAStreamingCallback
):
    """AsyncStreamingResponseCallback handler for BaseQAWithSources."""

    pass


@register_websocket_callback("BaseQAWithSources")
class AsyncBaseQAWithSourcesChainWebsocketCallback(
    AsyncBaseRetrievalQAWebsocketCallback
):
    """AsyncWebsocketCallback handler for BaseQAWithSources."""

    pass


@register_streaming_callback("QAWithSourcesChain")
class AsyncQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for QAWithSourcesChain."""

    pass


@register_websocket_callback("QAWithSourcesChain")
class AsyncQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for QAWithSourcesChain."""

    pass


@register_streaming_callback("VectorDBQAWithSourcesChain")
class AsyncVectorDBQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for VectorDBQAWithSourcesChain."""

    pass


@register_websocket_callback("VectorDBQAWithSourcesChain")
class AsyncVectorDBQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for VectorDBQAWithSourcesChain."""

    pass


@register_streaming_callback("RetrievalQAWithSourcesChain")
class AsyncRetrievalQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for RetrievalQAWithSourcesChain."""

    pass


@register_websocket_callback("RetrievalQAWithSourcesChain")
class AsyncRetrievalQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for RetrievalQAWithSourcesChain."""

    pass


@register_streaming_callback("ConversationalRetrievalChain")
class AsyncConversationalRetrievalChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for ConversationalRetrievalChain."""

    pass


@register_websocket_callback("ConversationalRetrievalChain")
class AsyncConversationalRetrievalChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for ConversationalRetrievalChain."""

    pass
