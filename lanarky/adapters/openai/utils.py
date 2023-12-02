import re
from typing import Any, Awaitable, Callable

from fastapi import Depends
from pydantic import BaseModel, create_model
from starlette.routing import compile_path

from lanarky.events import Events
from lanarky.logging import logger
from lanarky.utils import model_dump, model_fields
from lanarky.websockets import WebSocket, WebsocketSession

from .resources import ChatCompletion, ChatCompletionResource, Message, OpenAIResource
from .responses import HTTPStatusDetail, StreamingResponse, status


def build_factory_api_endpoint(
    path: str, endpoint: Callable[..., Any]
) -> Callable[..., Awaitable[Any]]:
    """Build a factory endpoint for API routes.

    Args:
        path: The path for the route.
        endpoint: openai resource factory function.
    """
    resource = compile_openai_resource_factory(endpoint)

    # index 1 of `compile_path` contains path_format output
    model_prefix = compile_model_prefix(compile_path(path)[1], resource)
    request_model = create_request_model(resource, model_prefix)

    async def factory_endpoint(
        request: request_model, resource: OpenAIResource = Depends(endpoint)
    ):
        return StreamingResponse(resource=resource, **model_dump(request))

    return factory_endpoint


def build_factory_websocket_endpoint(
    path: str, endpoint: Callable[..., Any]
) -> Callable[..., Awaitable[Any]]:
    """Build a factory endpoint for WebSocket routes.

    Args:
        path: The path for the route.
        endpoint: openai resource factory function.
    """
    resource = compile_openai_resource_factory(endpoint)

    # index 1 of `compile_path` contains path_format output
    model_prefix = compile_model_prefix(compile_path(path)[1], resource)
    request_model = create_request_model(resource, model_prefix)

    async def factory_endpoint(
        websocket: WebSocket, resource: OpenAIResource = Depends(endpoint)
    ):
        async with WebsocketSession().connect(websocket) as session:
            async for data in session:
                try:
                    async for chunk in resource.stream_response(
                        **model_dump(request_model(**data))
                    ):
                        await websocket.send_json(
                            dict(
                                data=chunk,
                                event=Events.COMPLETION,
                            )
                        )
                except Exception as e:
                    logger.error(f"openai error: {e}")
                    await websocket.send_json(
                        dict(
                            data=dict(
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=HTTPStatusDetail.INTERNAL_SERVER_ERROR,
                            ),
                            event=Events.ERROR,
                        )
                    )
                await websocket.send_json(dict(data="", event=Events.END))

    return factory_endpoint


def compile_openai_resource_factory(endpoint: Callable[..., Any]) -> OpenAIResource:
    """Compile an OpenAI resource factory function.

    Args:
        endpoint: openai resource factory function.

    Returns:
        An OpenAIResource instance.
    """
    try:
        resource = endpoint()
    except TypeError:
        raise TypeError("set default values for all factory endpoint parameters")

    if not isinstance(resource, OpenAIResource):
        raise TypeError("factory endpoint must return a LanarkyOpenAIResource instance")
    return resource


def compile_model_prefix(path: str, resource: OpenAIResource) -> str:
    """Compile a prefix for pydantic models.

    Args:
        path: The path for the route.
        resource: An OpenAIResource instance.
    """
    # Remove placeholders like '{item}' using regex
    path_wo_params = re.sub(r"\{.*?\}", "", path)
    path_prefix = "".join([part.capitalize() for part in path_wo_params.split("/")])

    resource_prefix = resource.__class__.__name__

    return f"{path_prefix}{resource_prefix}"


def create_request_model(
    resource: ChatCompletionResource, prefix: str = ""
) -> BaseModel:
    """Create a pydantic model for incoming requests.

    Note: Support limited to ChatCompletion resource.

    Args:
        resource: An OpenAIResource instance.
        prefix: A prefix for the model name.
    """
    if not isinstance(resource, ChatCompletionResource):
        raise TypeError("resource must be a ChatCompletion instance")

    request_fields = {"messages": (list[Message], ...)}

    prefix = prefix or resource.__class__.__name__

    return create_model(f"{prefix}Request", **request_fields)


def create_response_model(
    resource: ChatCompletionResource, prefix: str = None
) -> BaseModel:
    """Create a pydantic model for responses.

    Note: Support limited to ChatCompletion resource.

    Args:
        resource: An OpenAIResource instance.
        prefix: A prefix for the model name.
    """
    if not isinstance(resource, ChatCompletionResource):
        raise TypeError("resource must be a ChatCompletion instance")

    response_fields = {
        k: (v.annotation, ...) for k, v in model_fields(ChatCompletion).items()
    }

    prefix = prefix or resource.__class__.__name__

    return create_model(f"{prefix}Response", **response_fields)
