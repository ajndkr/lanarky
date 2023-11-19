import inspect
from typing import Any, Callable

from fastapi.datastructures import Default
from fastapi.routing import APIRoute

from .utils import build_factory_endpoint


class LangchainAPIRoute(APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),
        **kwargs
    ) -> None:
        # NOTE: LangchainAPIRoute is initialised again when
        # router is included in app. This is a hack to
        # build the factory endpoint only once.
        if not inspect.iscoroutinefunction(endpoint):
            factory_endpoint = build_factory_endpoint(path, endpoint)
            super().__init__(
                path, factory_endpoint, response_model=response_model, **kwargs
            )
        else:
            super().__init__(path, endpoint, response_model=response_model, **kwargs)
