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
            return await chain.acall(
                inputs=inputs, callbacks=[AsyncLLMChainStreamingCallback(send=send)]
            )

        return wrapper
