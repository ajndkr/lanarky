from typing import Any, Callable, Optional

from fastapi import params
from langchain.chains.base import Chain

from lanarky.adapters.langchain.utils import create_request_model, create_response_model
from lanarky.utils import model_dump


def Depends(
    dependency: Optional[Callable[..., Any]],
    *,
    dependency_kwargs: dict[str, Any] = {},
    use_cache: bool = True
) -> params.Depends:
    """Dependency injection for LangChain.

    Args:
        dependency: a "dependable" chain factory callable.
        dependency_kwargs: kwargs to pass to chain dependency.
        use_cache: use_cache parameter of `fastapi.Depends`.
    """
    try:
        chain = dependency()
    except TypeError:
        raise TypeError("set default values for all dependency parameters")

    if not isinstance(chain, Chain):
        raise TypeError("dependency must return a Chain instance")

    request_model = create_request_model(chain)
    response_model = create_response_model(chain)

    async def chain_dependency(
        request: request_model,
        chain: Chain = params.Depends(dependency, use_cache=use_cache),
    ) -> response_model:
        return await chain.acall(inputs=model_dump(request), **dependency_kwargs)

    return params.Depends(chain_dependency, use_cache=use_cache)
