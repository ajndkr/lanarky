from typing import Any, Awaitable, Callable

from fastapi import WebSocket
from langchain.chains.retrieval_qa.base import BaseRetrievalQA

from ..callbacks import AsyncLLMChainWebsocketCallback, AsyncWebsocketCallback
from ..schemas import WebsocketResponse
from .base import BaseLangchainWebsocketConnection


class RetrievalQAWebsocketConnection(BaseLangchainWebsocketConnection):
    """BaseLangchainWebsocketConnection class wrapper for BaseRetrievalQA instances."""

    @staticmethod
    def _create_chain_executor(
        chain: BaseRetrievalQA,
        websocket: WebSocket,
        response: WebsocketResponse,
    ) -> Callable[[], Awaitable[Any]]:
        async def wrapper(user_message: str):
            chain.combine_documents_chain.llm_chain.llm.callbacks = [
                AsyncLLMChainWebsocketCallback(websocket=websocket, response=response)
            ]
            return await chain.acall(
                inputs=user_message,
                callbacks=[
                    AsyncWebsocketCallback(websocket=websocket, response=response)
                ],
            )

        return wrapper
