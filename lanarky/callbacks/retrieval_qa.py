from typing import Any

from lanarky.register import (
    register_streaming_callback,
    register_streaming_json_callback,
    register_websocket_callback,
)
from lanarky.schemas import BaseRetrievalQAStreamingJSONResponse

from .llm import (
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainStreamingJSONCallback,
    AsyncLLMChainWebsocketCallback,
)

SUPPORTED_CHAINS = [
    "RetrievalQA",
    "ConversationRetrievalQA",
    "VectorDBQA",
    "QAWithSourcesChain",
    "VectorDBQAWithSourcesChain",
    "RetrievalQAWithSourcesChain",
    "ConversationalRetrievalChain",
]
SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
{document_metadata}
"""


@register_streaming_callback(SUPPORTED_CHAINS)
class AsyncBaseRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS:\n")
            await self.send(message)
            for document in outputs["source_documents"]:
                document_metadata = "\n".join(
                    [f"{k}: {v}" for k, v in document.metadata.items()]
                )
                message = self._construct_message(
                    self.source_document_template.format(
                        page_content=document.page_content,
                        document_metadata=document_metadata,
                    )
                )
                await self.send(message)


@register_websocket_callback(SUPPORTED_CHAINS)
class AsyncBaseRetrievalQAWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS:\n")
            await self.websocket.send_json(message)
            for document in outputs["source_documents"]:
                document_metadata = "\n".join(
                    [f"{k}: {v}" for k, v in document.metadata.items()]
                )
                message = self._construct_message(
                    self.source_document_template.format(
                        page_content=document.page_content,
                        document_metadata=document_metadata,
                    )
                )
                await self.websocket.send_json(message)


@register_streaming_json_callback(SUPPORTED_CHAINS)
class AsyncBaseRetrievalQAStreamingJSONCallback(AsyncLLMChainStreamingJSONCallback):
    """AsyncStreamingJSONResponseCallback handler for BaseRetrievalQA."""

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            source_documents = [
                document.dict() for document in outputs["source_documents"]
            ]
            message = self._construct_message(
                BaseRetrievalQAStreamingJSONResponse(source_documents=source_documents)
            )
            await self.send(message)
