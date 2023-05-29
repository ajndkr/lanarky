from typing import Any, Optional, Type

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from langchain.chains.base import Chain

from .utils import (
    StreamingMode,
    create_langchain_dependency,
    create_langchain_endpoint,
    create_langchain_websocket_endpoint,
    create_request_from_langchain_dependency,
    create_response_model_from_langchain_dependency,
)


class LangchainRouter(APIRouter):
    def __init__(
        self,
        *,
        langchain_url: Optional[str] = None,
        langchain_object: Optional[Type[Chain]] = None,
        langchain_endpoint_kwargs: Optional[dict[str, Any]] = None,
        streaming_mode: Optional[StreamingMode] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.langchain_url = langchain_url
        self.langchain_object = langchain_object
        self.langchain_endpoint_kwargs = langchain_endpoint_kwargs or {}
        self.streaming_mode = streaming_mode

        self.langchain_dependencies = []

        self.setup()

    def setup(self) -> None:
        """Sets up the Langchain router."""
        if self.langchain_url:
            self.add_langchain_api_route(
                self.langchain_url,
                self.langchain_object,
                self.streaming_mode,
                **self.langchain_endpoint_kwargs,
            )

    def add_langchain_api_route(
        self,
        url: str,
        langchain_object: Chain,
        streaming_mode: StreamingMode,
        methods: list[str] = ["POST"],
        **kwargs,
    ):
        """Adds a Langchain API route to the router."""
        langchain_dependency = create_langchain_dependency(langchain_object)
        endpoint_request = create_request_from_langchain_dependency(
            langchain_dependency
        )
        response_model = (
            create_response_model_from_langchain_dependency(langchain_dependency)
            if streaming_mode == StreamingMode.OFF
            else None
        )
        endpoint = create_langchain_endpoint(
            endpoint_request,
            langchain_dependency,
            response_model,
            streaming_mode,
        )

        self.add_api_route(
            url,
            endpoint,
            response_model=response_model,
            methods=methods,
            **kwargs,
        )

        self.langchain_dependencies.append(langchain_dependency)

    def add_langchain_api_websocket_route(self, url: str, langchain_object: Chain):
        """Adds a Langchain API websocket route to the router."""
        langchain_dependency = create_langchain_dependency(langchain_object)
        endpoint = create_langchain_websocket_endpoint(
            WebSocket,
            langchain_dependency,
        )

        self.add_api_websocket_route(url, endpoint)

        self.langchain_dependencies.append(langchain_dependency)
