from functools import lru_cache
from typing import Type

from fastapi import Depends, params
from langchain.chains.base import Chain
from pydantic import BaseModel, create_model

from lanarky.responses import StreamingResponse


def create_langchain_dependency(langchain_object: Type[Chain]) -> params.Depends:
    """Creates a langchain object dependency."""

    @lru_cache(maxsize=1)
    def dependency() -> Chain:
        return langchain_object

    return Depends(dependency)


def create_request_from_langchain_dependency(
    langchain_dependency: params.Depends,
) -> Type[BaseModel]:
    langchain_object: Chain = langchain_dependency.dependency()
    return create_model(
        "LangchainRequest", **{key: (str, "") for key in langchain_object.input_keys}
    )


def create_response_model_from_langchain_dependency(
    langchain_dependency: params.Depends,
) -> Type[BaseModel]:
    """Creates a response model from a langchain dependency."""
    langchain_object: Chain = langchain_dependency.dependency()
    return create_model(
        "LangchainResponse", **{key: (str, "") for key in langchain_object.output_keys}
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
        print(f"langchain_object: {langchain_object}")
        inputs = request.dict()
        print(f"inputs: {inputs}")
        return StreamingResponse.from_chain(
            langchain_object, inputs, media_type="text/event-stream"
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
