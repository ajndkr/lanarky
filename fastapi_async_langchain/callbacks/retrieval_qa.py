from typing import Any, Dict

from .base import AsyncFastApiStreamingCallback


class RetrievalQAFastApiStreamingCallback(AsyncFastApiStreamingCallback):
    """Async Callback handler for FastAPI StreamingResponse to RetrievalQA."""

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if outputs["source_documents"] is not None:
            await self.send("\n\nSOURCE DOCUMENTS: \n")
            if outputs["source_documents"] is not None:
                for doc in outputs["source_documents"]:
                    await self.send(f"page content: {doc.page_content} \n")
                    await self.send(f"source: {doc.metadata['source']} \n\n")
