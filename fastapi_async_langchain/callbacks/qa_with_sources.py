from .retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)


class AsyncBaseQAWithSourcesChainStreamingCallback(
    AsyncBaseRetrievalQAStreamingCallback
):
    """AsyncStreamingResponseCallback handler for BaseQAWithSources."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "BaseQAWithSources"


class AsyncBaseQAWithSourcesChainWebsocketCallback(
    AsyncBaseRetrievalQAWebsocketCallback
):
    """AsyncWebsocketCallback handler for BaseQAWithSources."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "BaseQAWithSources"


class AsyncQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for QAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "QAWithSourcesChain"


class AsyncQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for QAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "QAWithSourcesChain"


class AsyncVectorDBQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for VectorDBQAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "VectorDBQAWithSourcesChain"


class AsyncVectorDBQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for VectorDBQAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "VectorDBQAWithSourcesChain"


class AsyncRetrievalQAWithSourcesChainStreamingCallback(
    AsyncBaseQAWithSourcesChainStreamingCallback
):
    """AsyncStreamingResponseCallback handler for RetrievalQAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "RetrievalQAWithSourcesChain"


class AsyncRetrievalQAWithSourcesChainWebsocketCallback(
    AsyncBaseQAWithSourcesChainWebsocketCallback
):
    """AsyncWebsocketCallback handler for RetrievalQAWithSourcesChain."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "RetrievalQAWithSourcesChain"
