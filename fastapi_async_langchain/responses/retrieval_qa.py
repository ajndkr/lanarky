from typing import Any, Awaitable, Callable, Dict, Union

from langchain.callbacks import AsyncCallbackManager
from langchain.chains.retrieval_qa.base import BaseRetrievalQA
from starlette.types import Send

from ..callbacks import (
    AsyncLLMChainStreamingCallback,
    AsyncRetrievalQAStreamingCallback,
    AsyncStreamingResponseCallback,
)
from .base import BaseLangchainStreamingResponse


class RetrievalQAStreamingResponse(BaseLangchainStreamingResponse):
    """BaseLangchainStreamingResponse class wrapper for BaseRetrievalQA instances."""

    @staticmethod
    def _create_chain_executor(
        chain: BaseRetrievalQA, inputs: Union[Dict[str, Any], Any]
    ) -> Callable[[Send], Awaitable[Any]]:
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
                if isinstance(handler, AsyncStreamingResponseCallback):
                    chain.combine_documents_chain.llm_chain.llm.callback_manager.remove_handler(
                        handler
                    )
                    break
            chain.combine_documents_chain.llm_chain.llm.callback_manager.add_handler(
                AsyncLLMChainStreamingCallback(send=send)
            )

            if not isinstance(chain.callback_manager, AsyncCallbackManager):
                raise TypeError(
                    "chain.callback_manager must be an instance of AsyncCallbackManager"
                )
            for handler in chain.callback_manager.handlers:
                if isinstance(handler, AsyncStreamingResponseCallback):
                    chain.callback_manager.remove_handler(handler)
                    break
            chain.callback_manager.add_handler(
                AsyncRetrievalQAStreamingCallback(send=send)
            )

            return await chain.acall(inputs)

        return wrapper
