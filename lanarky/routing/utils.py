from enum import IntEnum
from functools import lru_cache
from typing import Type

from fastapi import Depends, WebSocket, params
from langchain.chains.base import Chain
from pydantic import BaseModel, create_model

from lanarky.responses import StreamingResponse
from lanarky.websockets import WebsocketConnection


class StreamingMode(IntEnum):
    OFF = 0
    TEXT = 1
    JSON = 2


class LLMCacheMode(IntEnum):
    OFF = 0
    IN_MEMORY = 1
    REDIS = 2
    GPTCACHE = 3


def create_langchain_dependency(langchain_object: Type[Chain]) -> params.Depends:
    """Creates a langchain object dependency."""

    @lru_cache(maxsize=1)
    def dependency() -> Chain:
        return langchain_object

    return Depends(dependency)


def create_request_from_langchain_dependency(
    langchain_dependency: params.Depends, name_prefix: str = ""
) -> Type[BaseModel]:
    langchain_object: Chain = langchain_dependency.dependency()
    model_name = name_prefix + "LangchainRequest"
    return create_model(
        model_name,
        **{key: (str, "") for key in langchain_object.input_keys},
    )


def create_response_model_from_langchain_dependency(
    langchain_dependency: params.Depends, name_prefix: str = ""
) -> Type[BaseModel]:
    """Creates a response model from a langchain dependency."""
    langchain_object: Chain = langchain_dependency.dependency()
    model_name = name_prefix + "LangchainResponse"
    return create_model(
        model_name,
        **{key: (str, "") for key in langchain_object.output_keys},
    )


def create_langchain_base_endpoint(
    endpoint_request: BaseModel,
    langchain_dependency: params.Depends,
    response_model: BaseModel,
):
    async def endpoint(
        request: endpoint_request,
        langchain_object: Chain = langchain_dependency,
    ) -> response_model:
        """Base chat endpoint."""
        return await langchain_object.acall(inputs=request.dict())

    return endpoint


def create_langchain_streaming_endpoint(
    endpoint_request: BaseModel, langchain_dependency: params.Depends
):
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
    """Creates a Langchain endpoint."""
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
    websocket: Type[WebSocket], langchain_dependency: params.Depends
):
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
