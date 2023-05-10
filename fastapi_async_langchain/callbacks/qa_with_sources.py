from .retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)


class AsyncBaseQAWithSourcesChainStreamingCallback(
    AsyncBaseRetrievalQAStreamingCallback
):
    """AsyncStreamingResponseCallback handler for BaseQAWithSources."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "BaseQAWithSources"


class AsyncBaseQAWithSourcesChainWebsocketCallback(
    AsyncBaseRetrievalQAWebsocketCallback
):
    """AsyncWebsocketCallback handler for BaseQAWithSources."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "BaseQAWithSources"


class AsyncQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for QAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "QAWithSourcesChain"


class AsyncQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for QAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "QAWithSourcesChain"


class AsyncVectorDBQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for VectorDBQAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "VectorDBQAWithSourcesChain"


class AsyncVectorDBQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for VectorDBQAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "VectorDBQAWithSourcesChain"


class AsyncRetrievalQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for RetrievalQAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "RetrievalQAWithSourcesChain"


class AsyncRetrievalQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for RetrievalQAWithSourcesChain."""

    @property
    def chain_type(self) -> str:
        """The chain type."""
        return "RetrievalQAWithSourcesChain"
