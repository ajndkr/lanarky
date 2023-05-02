from typing import Any, Awaitable, Callable, Dict, Union

from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager
from starlette.types import Send

from ..callbacks import AsyncLLMChainStreamingCallback, AsyncStreamingResponseCallback
from .base import BaseLangchainStreamingResponse


class LLMChainStreamingResponse(BaseLangchainStreamingResponse):
    """BaseLangchainStreamingResponse class wrapper for LLMChain instances."""

    @staticmethod
    def _create_chain_executor(
        chain: LLMChain, inputs: Union[Dict[str, Any], Any]
    ) -> Callable[[Send], Awaitable[Any]]:
        async def wrapper(send: Send):
            if not isinstance(chain.llm.callback_manager, AsyncCallbackManager):
                raise TypeError(
                    "llm.callback_manager must be an instance of AsyncCallbackManager"
                )
            for handler in chain.llm.callback_manager.handlers:
                if isinstance(handler, AsyncStreamingResponseCallback):
                    chain.llm.callback_manager.remove_handler(handler)
                    break
            chain.llm.callback_manager.add_handler(
                AsyncLLMChainStreamingCallback(send=send)
            )
            return await chain.arun(inputs)

        return wrapper
