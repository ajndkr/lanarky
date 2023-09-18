from enum import IntEnum
from functools import lru_cache
from typing import Type

from fastapi import Depends, WebSocket, params
from langchain.chains.base import Chain
from langchain.schema import Document
from pydantic import BaseModel, create_model

from lanarky.responses import StreamingResponse
from lanarky.websockets import WebsocketConnection


class StreamingMode(IntEnum):
    """Streaming modes for LangchainRouter."""

    OFF = 0
    TEXT = 1
    JSON = 2


class LLMCacheMode(IntEnum):
    """LLM cache modes for LangchainRouter."""

    OFF = 0
    IN_MEMORY = 1
    REDIS = 2
    GPTCACHE = 3


BASE_LANGCHAIN_TYPES = [
    "LLMChain",
    "ConversationChain",
    "AgentExecutor",
    "RetrievalQAWithSourcesChain",
    "ConversationalRetrievalChain",
]
ERROR_MESSAGE = """Error! Creating a {model_type} model for '{chain_type}' is not currently supported by 'LangchainRouter.add_langchain_api_route()'.
Available chain types: {chain_types}

To use a custom chain type, you must define your own FastAPI endpoint.
"""
CHAT_HISTORY_KEY = "chat_history"
SOURCE_DOCUMENTS_KEY = "source_documents"


def create_langchain_dependency(langchain_object: Type[Chain]) -> params.Depends:
    """Creates a langchain object dependency.

    Args:
        langchain_object: The langchain object.
    """

    @lru_cache(maxsize=1)
    def dependency() -> Chain:
        return langchain_object

    return Depends(dependency)


def create_request_from_langchain_dependency(
    langchain_dependency: params.Depends, name_prefix: str = ""
) -> Type[BaseModel]:
    """Creates a request model from a langchain dependency.

    Args:
        langchain_dependency: The langchain dependency.
        name_prefix: The name prefix for the model.
    """
    langchain_object: Chain = langchain_dependency.dependency()
    langchain_object_name = str(langchain_object.__class__.__name__)
    model_name = f"{name_prefix}{langchain_object_name}Request"

    additional_keys = (
        {CHAT_HISTORY_KEY: (list[tuple[str, str]], ...)}
        if langchain_object_name == "ConversationalRetrievalChain"
        else {}
    )

    if langchain_object_name in BASE_LANGCHAIN_TYPES:
        return create_model(
            model_name,
            **{
                **{key: (str, ...) for key in langchain_object.input_keys},
                **additional_keys,
            },
        )
    else:
        raise TypeError(
            ERROR_MESSAGE.format(
                model_type="Request",
                chain_type=langchain_object_name,
                chain_types=BASE_LANGCHAIN_TYPES,
            )
        )


def create_response_model_from_langchain_dependency(
    langchain_dependency: params.Depends, name_prefix: str = ""
) -> Type[BaseModel]:
    """Creates a response model from a langchain dependency.

    Args:
        langchain_dependency: The langchain dependency.
        name_prefix: The name prefix for the model.
    """
    langchain_object: Chain = langchain_dependency.dependency()
    langchain_object_name = str(langchain_object.__class__.__name__)
    model_name = f"{name_prefix}{langchain_object_name}Response"

    additional_keys = (
        {SOURCE_DOCUMENTS_KEY: (list[Document], ...)}
        if hasattr(langchain_object, "return_source_documents")
        and langchain_object.return_source_documents
        else {}
    )

    if langchain_object_name in BASE_LANGCHAIN_TYPES:
        return create_model(
            model_name,
            **{
                **{key: (str, ...) for key in langchain_object.output_keys},
                **additional_keys,
            },
        )
    else:
        raise TypeError(
            ERROR_MESSAGE.format(
                model_type="Response",
                chain_type=langchain_object_name,
                chain_types=BASE_LANGCHAIN_TYPES,
            )
        )


def create_langchain_base_endpoint(
    endpoint_request: BaseModel,
    langchain_dependency: params.Depends,
    response_model: BaseModel,
):
    """Creates a base Langchain endpoint.

    Args:
        endpoint_request: The request model.
        langchain_dependency: The langchain dependency.
        response_model: The response model.
    """

    async def endpoint(
        request: endpoint_request,
        langchain_object: Chain = langchain_dependency,
    ) -> response_model:
        """Base chat endpoint."""
        return await langchain_object.acall(
            inputs=request.dict(), return_only_outputs=True
        )

    return endpoint


def create_langchain_streaming_endpoint(
    endpoint_request: BaseModel, langchain_dependency: params.Depends
):
    """Creates a streaming Langchain endpoint.

    Args:
        endpoint_request: The request model.
        langchain_dependency: The langchain dependency.
    """

    async def endpoint(
        request: endpoint_request,
        langchain_object: Chain = langchain_dependency,
    ) -> StreamingResponse:
        """Streaming chat endpoint."""
        return StreamingResponse.from_chain(
            langchain_object, request.dict(), media_type="text/event-stream"
        )

    return endpoint


def create_langchain_streaming_json_endpoint(
    endpoint_request: BaseModel, langchain_dependency: params.Depends
):
    """Creates a streaming JSON Langchain endpoint.

    Args:
        endpoint_request: The request model.
        langchain_dependency: The langchain dependency.
    """

    async def endpoint(
        request: endpoint_request,
        langchain_object: Chain = langchain_dependency,
    ) -> StreamingResponse:
        """Streaming JSON chat endpoint."""
        return StreamingResponse.from_chain(
            langchain_object,
            request.dict(),
            as_json=True,
            media_type="text/event-stream",
        )

    return endpoint


def create_langchain_endpoint(
    endpoint_request: BaseModel,
    langchain_dependency: params.Depends,
    response_model: BaseModel,
    streaming_mode: StreamingMode,
):
    """Creates a Langchain endpoint based on the streaming mode.

    Args:
        endpoint_request: The request model.
        langchain_dependency: The langchain dependency.
        response_model: The response model.
        streaming_mode: The streaming mode.
    """
    if streaming_mode == StreamingMode.OFF:
        endpoint = create_langchain_base_endpoint(
            endpoint_request, langchain_dependency, response_model
        )
    elif streaming_mode == StreamingMode.TEXT:
        endpoint = create_langchain_streaming_endpoint(
            endpoint_request, langchain_dependency
        )
    elif streaming_mode == StreamingMode.JSON:
        endpoint = create_langchain_streaming_json_endpoint(
            endpoint_request, langchain_dependency
        )
    else:
        raise ValueError(f"Invalid streaming mode: {streaming_mode}")

    return endpoint


def create_langchain_websocket_endpoint(
    websocket: WebSocket, langchain_dependency: params.Depends
):
    """Creates a websocket Langchain endpoint.

    Args:
        websocket: The websocket model.
        langchain_dependency: The langchain dependency.
    """

    async def endpoint(
        websocket: websocket,
        langchain_object: Chain = langchain_dependency,
    ) -> None:
        """Websocket chat endpoint."""
        connection = WebsocketConnection.from_chain(
            chain=langchain_object, websocket=websocket
        )
        await connection.connect()

    return endpoint
