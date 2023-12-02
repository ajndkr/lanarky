from typing import Any, Callable, Optional

from fastapi import params

from lanarky.utils import model_dump

from .resources import OpenAIResource
from .utils import create_request_model, create_response_model


def Depends(
    dependency: Optional[Callable[..., Any]],
    *,
    dependency_kwargs: dict[str, Any] = {},
    use_cache: bool = True
) -> params.Depends:
    """Dependency injection for OpenAI.

    Args:
        dependency: a "dependable" resource factory callable.
        dependency_kwargs: kwargs to pass to resource dependency.
        use_cache: use_cache parameter of `fastapi.Depends`.
    """
    try:
        resource = dependency()
    except TypeError:
        raise TypeError("set default values for all dependency parameters")

    if not isinstance(resource, OpenAIResource):
        raise TypeError("dependency must return a OpenAIResource instance")

    request_model = create_request_model(resource)
    response_model = create_response_model(resource)

    async def resource_dependency(
        request: request_model,
        resource: OpenAIResource = params.Depends(dependency, use_cache=use_cache),
    ) -> response_model:
        resource_kwargs = {**model_dump(request), **dependency_kwargs}

        return await resource(**resource_kwargs)

    return params.Depends(resource_dependency, use_cache=use_cache)
