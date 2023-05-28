from enum import IntEnum
from typing import Any, Type

from fastapi.routing import APIRouter
from langchain.chains.base import Chain

from .utils import (
    create_langchain_base_endpoint,
    create_langchain_dependency,
    create_langchain_streaming_endpoint,
    create_langchain_streaming_json_endpoint,
    create_request_from_langchain_dependency,
    create_response_model_from_langchain_dependency,
)


class StreamingMode(IntEnum):
    OFF = 0
    TEXT = 1
    JSON = 2


def create_langchain_endpoint(
    endpoint_request, langchain_dependency, response_model, streaming_mode
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


class LangchainRouter(APIRouter):
    def __init__(
        self,
        *,
        langchain_url: str = "/chat",
        langchain_object: Type[Chain] = Chain,
        langchain_endpoint_kwargs: dict[str, Any] = None,
        streaming_mode: StreamingMode = StreamingMode.OFF,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.langchain_url = langchain_url
        self.langchain_object = langchain_object
        self.langchain_endpoint_kwargs = langchain_endpoint_kwargs or {}
        self.streaming_mode = streaming_mode

        self.langchain_dependency = create_langchain_dependency(langchain_object)

        self.setup()

    def setup(self) -> None:
        if self.langchain_url:
            endpoint_request = create_request_from_langchain_dependency(
                self.langchain_dependency
            )
            response_model = (
                create_response_model_from_langchain_dependency(
                    self.langchain_dependency
                )
                if self.streaming_mode == StreamingMode.OFF
                else None
            )
            endpoint = create_langchain_endpoint(
                endpoint_request,
                self.langchain_dependency,
                response_model,
                self.streaming_mode,
            )

            self.add_api_route(
                self.langchain_url,
                endpoint,
                response_model=response_model,
                methods=["POST"],
                **self.langchain_endpoint_kwargs,
            )
