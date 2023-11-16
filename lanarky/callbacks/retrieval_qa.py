from typing import Any, cast

from langchain.schema import Document

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
SOURCE_DOCUMENTS_KEY = "source_documents"


@register_streaming_callback(SUPPORTED_CHAINS)
class AsyncBaseRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for BaseRetrievalQA."""

    def __init__(
        self, source_document_template: str = SOURCE_DOCUMENT_TEMPLATE, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.source_document_template = source_document_template

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if self.llm_cache_enabled:
            await super().on_chain_end(outputs, **kwargs)
        if SOURCE_DOCUMENTS_KEY in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS:\n")
            await self.send(message)
            for document in outputs[SOURCE_DOCUMENTS_KEY]:
                document = cast(Document, document)
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

    def __init__(
        self, source_document_template: str = SOURCE_DOCUMENT_TEMPLATE, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.source_document_template = source_document_template

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if self.llm_cache_enabled:
            await super().on_chain_end(outputs, **kwargs)
        if SOURCE_DOCUMENTS_KEY in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS:\n")
            await self.websocket.send_json(message)
            for document in outputs[SOURCE_DOCUMENTS_KEY]:
                document = cast(Document, document)
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
        if self.llm_cache_enabled:
            await super().on_chain_end(outputs, **kwargs)
        if SOURCE_DOCUMENTS_KEY in outputs:
            # NOTE: langchain is using pydantic_v1 for `Document`
            source_documents: list[dict] = [
                document.dict() for document in outputs[SOURCE_DOCUMENTS_KEY]
            ]
            message = self._construct_message(
                BaseRetrievalQAStreamingJSONResponse(source_documents=source_documents)
            )
            await self.send(message)
