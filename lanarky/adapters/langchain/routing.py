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
        factory_endpoint = build_factory_endpoint(path, endpoint)
        super().__init__(
            path, factory_endpoint, response_model=response_model, **kwargs
        )
