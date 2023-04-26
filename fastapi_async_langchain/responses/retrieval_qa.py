from typing import Any, Dict, Union

from langchain.callbacks import AsyncCallbackManager
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from starlette.types import Send

from ..callbacks import RetrievalQAFastApiStreamingCallback
from .base import BaseLangchainStreamingResponse


class RetrievalQAStreamingResponse(BaseLangchainStreamingResponse):
    """BaseLangchainStreamingResponse class wrapper for BaseRetrievalQA instances."""

    @staticmethod
    def chain_wrapper_fn(chain: BaseRetrievalQA, inputs: Union[Dict[str, Any], Any]):
        async def wrapper(send: Send):
            if not isinstance(
                chain.combine_documents_chain.llm_chain.llm.callback_manager,
                AsyncCallbackManager,
            ):
                raise TypeError(
                    "llm.callback_manager must be an instance of AsyncCallbackManager"
                )
            for (
                handler
            ) in chain.combine_documents_chain.llm_chain.llm.callback_manager.handlers:
                if isinstance(handler, RetrievalQAFastApiStreamingCallback):
                    chain.combine_documents_chain.llm_chain.llm.callback_manager.remove_handler(
                        handler
                    )
                    break
            chain.combine_documents_chain.llm_chain.llm.callback_manager.add_handler(
                RetrievalQAFastApiStreamingCallback(send=send)
            )
            return await chain.acall(inputs)

        return wrapper
