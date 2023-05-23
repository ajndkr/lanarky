from lanarky.register import (
    register_streaming_callback,
    register_streaming_json_callback,
    register_websocket_callback,
)

from .retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAStreamingJSONCallback,
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


@register_streaming_json_callback("BaseQAWithSources")
class AsyncBaseQAWithSourcesChainStreamingJSONCallback(
    AsyncBaseRetrievalQAStreamingJSONCallback
):
    """AsyncStreamingJSONResponseCallback handler for BaseQAWithSources."""

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


@register_streaming_json_callback("QAWithSourcesChain")
class AsyncQAWithSourcesChainStreamingJSONCallback(
    AsyncBaseQAWithSourcesChainStreamingJSONCallback
):
    """AsyncStreamingJSONResponseCallback handler for QAWithSourcesChain."""

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


@register_streaming_json_callback("VectorDBQAWithSourcesChain")
class AsyncVectorDBQAWithSourcesChainStreamingJSONCallback(
    AsyncBaseQAWithSourcesChainStreamingJSONCallback
):
    """AsyncStreamingJSONResponseCallback handler for VectorDBQAWithSourcesChain."""

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


@register_streaming_json_callback("RetrievalQAWithSourcesChain")
class AsyncRetrievalQAWithSourcesChainStreamingJSONCallback(
    AsyncBaseQAWithSourcesChainStreamingJSONCallback
):
    """AsyncStreamingJSONResponseCallback handler for RetrievalQAWithSourcesChain."""

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


@register_streaming_json_callback("ConversationalRetrievalChain")
class AsyncConversationalRetrievalChainStreamingJSONCallback(
    AsyncBaseQAWithSourcesChainStreamingJSONCallback
):
    """AsyncStreamingJSONResponseCallback handler for ConversationalRetrievalChain."""

    pass
