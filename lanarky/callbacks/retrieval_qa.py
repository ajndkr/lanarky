from typing import Any, Dict

from lanarky.register import register_streaming_callback, register_websocket_callback

from .llm import AsyncLLMChainStreamingCallback, AsyncLLMChainWebsocketCallback

SOURCE_DOCUMENT_TEMPLATE = """
page content: {page_content}
source: {source}
"""


class AsyncBaseRetrievalQAStreamingCallback(AsyncLLMChainStreamingCallback):
    """AsyncStreamingResponseCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS: \n")
            await self.send(message)
            for document in outputs["source_documents"]:
                message = self._construct_message(
                    self.source_document_template.format(
                        page_content=document.page_content,
                        source=document.metadata["source"],
                    )
                )
                await self.send(message)


class AsyncBaseRetrievalQAWebsocketCallback(AsyncLLMChainWebsocketCallback):
    """AsyncWebsocketCallback handler for BaseRetrievalQA."""

    source_document_template: str = SOURCE_DOCUMENT_TEMPLATE

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            message = self._construct_message("\n\nSOURCE DOCUMENTS: \n")
            await self.websocket.send_json(message)
            for document in outputs["source_documents"]:
                message = self._construct_message(
                    self.source_document_template.format(
                        page_content=document.page_content,
                        source=document.metadata["source"],
                    )
                )
                await self.websocket.send_json(message)


@register_streaming_callback("RetrievalQA")
class AsyncRetrievalQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for RetrievalQA."""

    pass


@register_streaming_callback("VectorDBQA")
class AsyncVectorDBQAStreamingCallback(AsyncBaseRetrievalQAStreamingCallback):
    """AsyncStreamingResponseCallback handler for VectorDBQA."""

    pass


@register_websocket_callback("RetrievalQA")
class AsyncRetrievalQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for RetrievalQA."""

    pass


@register_websocket_callback("VectorDBQA")
class AsyncVectorDBQAWebsocketCallback(AsyncBaseRetrievalQAWebsocketCallback):
    """AsyncWebsocketCallback handler for VectorDBQA."""

    pass
