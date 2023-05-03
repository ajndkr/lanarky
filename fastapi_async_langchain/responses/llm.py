from typing import Any, Awaitable, Callable, Dict, Union

from langchain import LLMChain
from starlette.types import Send

from ..callbacks import AsyncLLMChainStreamingCallback
from .base import BaseLangchainStreamingResponse


class LLMChainStreamingResponse(BaseLangchainStreamingResponse):
    """BaseLangchainStreamingResponse class wrapper for LLMChain instances."""

    @staticmethod
    def _create_chain_executor(
        chain: LLMChain, inputs: Union[Dict[str, Any], Any]
    ) -> Callable[[Send], Awaitable[Any]]:
        async def wrapper(send: Send):
            callback = AsyncLLMChainStreamingCallback(send=send)
            return await chain.arun(input=inputs, callbacks=[callback])

        return wrapper
