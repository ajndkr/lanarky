from typing import Any, Dict

from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field
from starlette.types import Send


class AsyncFastApiStreamingCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI StreamingResponse."""

    send: Send = Field(...)

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        await self.send(token)

    async def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if not outputs['source_documents'] is None:
            source_documents = '\n'.join(f"{doc.page_content}: {doc.metadata['source']}" for doc in outputs['source_documents'])
            await self.send("\n\nSOURCE DOCUMENTS: \n" + source_documents)
