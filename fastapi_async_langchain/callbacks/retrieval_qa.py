from typing import Any, Dict

from .llm import AsyncLLMChainStreamingCallback, AsyncLLMChainWebsocketCallback

SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
source: {source}
"""


class AsyncRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for RetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

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


class AsyncRetrievalQAWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for RetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

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
