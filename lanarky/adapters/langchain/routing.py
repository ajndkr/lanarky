import inspect
from typing import Any, Callable, Optional, Sequence

from fastapi import params
from fastapi.datastructures import Default
from fastapi.routing import APIRoute, APIRouter, APIWebSocketRoute

from .utils import build_factory_api_endpoint, build_factory_websocket_endpoint


class LangchainAPIRoute(APIRoute):
    """APIRoute class for LangChain."""

    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),
        **kwargs: dict[str, Any],
    ) -> None:
        """Constructor method.

        Args:
            path: The path for the route.
            endpoint: The endpoint to call when the route is requested.
            response_model: The response model to use for the route.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """
        # NOTE: LangchainAPIRoute is initialised again when
        # router is included in app. This is a hack to
        # build the factory endpoint only once.
        if not inspect.iscoroutinefunction(endpoint):
            factory_endpoint = build_factory_api_endpoint(path, endpoint)
            super().__init__(
                path, factory_endpoint, response_model=response_model, **kwargs
            )
        else:
            super().__init__(path, endpoint, response_model=response_model, **kwargs)


class LangchainAPIWebSocketRoute(APIWebSocketRoute):
    """APIWebSocketRoute class for LangChain."""

    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        name: Optional[str] = None,
        **kwargs: dict[str, Any],
    ) -> None:
        """Constructor method.

        Args:
            path: The path for the route.
            endpoint: The endpoint to call when the route is requested.
            name: The name of the route.
            **kwargs: Keyword arguments to pass to the parent constructor.
        """
        super().__init__(path, endpoint, name=name, **kwargs)
        # NOTE: LangchainAPIRoute is initialised again when
        # router is included in app. This is a hack to
        # build the factory endpoint only once.
        if not inspect.iscoroutinefunction(endpoint):
            factory_endpoint = build_factory_websocket_endpoint(path, endpoint)
            super().__init__(path, factory_endpoint, name=name, **kwargs)
        else:
            super().__init__(path, endpoint, name=name, **kwargs)


class LangchainAPIRouter(APIRouter):
    """APIRouter class for LangChain."""

    def __init__(self, *, route_class: type[APIRoute] = LangchainAPIRoute, **kwargs):
        super().__init__(route_class=route_class, **kwargs)

    def add_api_websocket_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        name: Optional[str] = None,
        *,
        dependencies: Optional[Sequence[params.Depends]] = None,
    ) -> None:
        current_dependencies = self.dependencies.copy()
        if dependencies:
            current_dependencies.extend(dependencies)

        route = LangchainAPIWebSocketRoute(
            self.prefix + path,
            endpoint=endpoint,
            name=name,
            dependencies=current_dependencies,
            dependency_overrides_provider=self.dependency_overrides_provider,
        )
        self.routes.append(route)
