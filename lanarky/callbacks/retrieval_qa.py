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

SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
{document_metadata}
"""


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


@register_streaming_callback("RetrievalQA")
class AsyncRetrievalQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for RetrievalQA."""

    pass


@register_websocket_callback("RetrievalQA")
class AsyncRetrievalQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for RetrievalQA."""

    pass


@register_streaming_json_callback("RetrievalQA")
class AsyncRetrievalQAStreamingJSONCallback(AsyncBaseRetrievalQAStreamingJSONCallback):
    """AsyncStreamingJSONResponseCallback handler for RetrievalQA."""

    pass


@register_streaming_callback("VectorDBQA")
class AsyncVectorDBQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for VectorDBQA."""

    pass


@register_websocket_callback("VectorDBQA")
class AsyncVectorDBQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for VectorDBQA."""

    pass


@register_streaming_json_callback("VectorDBQA")
class AsyncVectorDBQAStreamingJSONCallback(AsyncBaseRetrievalQAStreamingJSONCallback):
    """AsyncStreamingJSONResponseCallback handler for VectorDBQA."""

    pass
