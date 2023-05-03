from typing import Any, Dict

from ..streaming.retrieval_qa import SOURCE_DOCUMENT_TEMPLATE
from .base import AsyncLLMChainWebsocketCallback


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
