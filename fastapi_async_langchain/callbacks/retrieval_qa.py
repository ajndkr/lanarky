from typing import Any, Dict

from .llm import AsyncLLMChainStreamingCallback, AsyncLLMChainWebsocketCallback

SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
source: {source}
"""


class AsyncBaseRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "BaseRetrievalQA"

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            await self.send("\n\nSOURCE DOCUMENTS: \n")
            for document in outputs["source_documents"]:
                await self.send(
                    self.source_document_template.format(
                        page_content=document.page_content,
                        source=document.metadata["source"],
                    )
                )


class AsyncBaseRetrievalQAWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "BaseRetrievalQA"

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            await self.websocket.send_json(
                {
                    **self.response.dict(),
                    **{"message": "\n\nSOURCE DOCUMENTS: \n"},
                }
            )
            for document in outputs["source_documents"]:
                source_document = self.source_document_template.format(
                    page_content=document.page_content,
                    source=document.metadata["source"],
                )
                await self.websocket.send_json(
                    {
                        **self.response.dict(),
                        **{"message": source_document},
                    }
                )


class AsyncRetrievalQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for RetrievalQA."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "RetrievalQA"


class AsyncVectorDBQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for VectorDBQA."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "VectorDBQA"


class AsyncRetrievalQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for RetrievalQA."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "RetrievalQA"


class AsyncVectorDBQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for VectorDBQA."""

    @staticmethod
    def get_chain_type() -> str:
        """The chain type."""
        return "VectorDBQA"
