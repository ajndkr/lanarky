from typing import Any, Awaitable, Callable, Dict, Union

from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from starlette.types import Send

from ..callbacks import AsyncRetrievalQAStreamingCallback
from .base import BaseLangchainStreamingResponse


class RetrievalQAStreamingResponse(BaseLangchainStreamingResponse):
    """BaseLangchainStreamingResponse class wrapper for BaseRetrievalQA instances."""

    @staticmethod
    def _create_chain_executor(
        chain: BaseRetrievalQA, inputs: Union[Dict[str, Any], Any]
    ) -> Callable[[Send], Awaitable[Any]]:
        async def wrapper(send: Send):
            return await chain.acall(
                inputs=inputs, callbacks=[AsyncRetrievalQAStreamingCallback(send=send)]
            )

        return wrapper
