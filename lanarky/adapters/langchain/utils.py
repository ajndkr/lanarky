import re
from typing import Any, Awaitable, Callable

from fastapi import Depends
from langchain.agents import AgentExecutor
from langchain.chains.base import Chain
from langchain.schema.document import Document
from pydantic import BaseModel, create_model
from starlette.routing import compile_path

from lanarky.adapters.langchain.callbacks import (
    FinalTokenStreamingCallbackHandler,
    FinalTokenWebSocketCallbackHandler,
    SourceDocumentsStreamingCallbackHandler,
    SourceDocumentsWebSocketCallbackHandler,
    TokenStreamingCallbackHandler,
    TokenWebSocketCallbackHandler,
)
from lanarky.adapters.langchain.responses import HTTPStatusDetail, StreamingResponse
from lanarky.events import Events
from lanarky.logging import logger
from lanarky.utils import model_dump
from lanarky.websockets import WebSocket, WebsocketSession


def build_factory_api_endpoint(
    path: str, endpoint: Callable[..., Any]
) -> Callable[..., Awaitable[Any]]:
    """Build a factory endpoint for API routes.

    Args:
        path: The path for the route.
        endpoint: LangChain instance factory function.
    """
    chain = compile_chain_factory(endpoint)

    # index 1 of `compile_path` contains path_format output
    model_prefix = compile_model_prefix(compile_path(path)[1], chain)
    request_model = create_request_model(chain, model_prefix)

    callbacks = get_streaming_callbacks(chain)

    async def factory_endpoint(
        request: request_model, chain: Chain = Depends(endpoint)
    ):
        return StreamingResponse(
            chain=chain, config={"inputs": model_dump(request), "callbacks": callbacks}
        )

    return factory_endpoint


def build_factory_websocket_endpoint(
    path: str, endpoint: Callable[..., Any]
) -> Callable[..., Awaitable[Any]]:
    """Build a factory endpoint for WebSocket routes.

    Args:
        path: The path for the route.
        endpoint: LangChain instance factory function.
    """
    chain = compile_chain_factory(endpoint)

    # index 1 of `compile_path` contains path_format output
    model_prefix = compile_model_prefix(compile_path(path)[1], chain)
    request_model = create_request_model(chain, model_prefix)

    async def factory_endpoint(websocket: WebSocket, chain: Chain = Depends(endpoint)):
        callbacks = get_websocket_callbacks(chain, websocket)
        async with WebsocketSession().connect(websocket) as session:
            async for data in session:
                try:
                    await chain.acall(
                        inputs=model_dump(request_model(**data)),
                        callbacks=callbacks,
                    )
                except Exception as e:
                    logger.error(f"langchain error: {e}")
                    await websocket.send_json(
                        dict(
                            data=dict(
                                status=500,
                                detail=HTTPStatusDetail(
                                    code=500,
                                    message="Internal Server Error",
                                ),
                            ),
                            event=Events.ERROR,
                        )
                    )
                await websocket.send_json(dict(data="", event=Events.END))

    return factory_endpoint


def compile_chain_factory(endpoint: Callable[..., Any]):
    """Compile a LangChain instance factory function.

    Args:
        endpoint: LangChain instance factory function.
    """
    try:
        chain = endpoint()
    except TypeError:
        raise TypeError("set default values for all factory endpoint parameters")

    if not isinstance(chain, Chain):
        raise TypeError("factory endpoint must return a Chain instance")
    return chain


def create_request_model(chain: Chain, prefix: str = "") -> BaseModel:
    """Create a pydantic request model for a LangChain instance.

    Args:
        chain: A LangChain instance.
        prefix: A prefix for the model name.
    """
    request_fields = {}

    for key in chain.input_keys:
        # TODO: add support for other input key types
        # based on demand
        if key == "chat_history":
            request_fields[key] = (list[tuple[str, str]], ...)
        else:
            request_fields[key] = (str, ...)

    prefix = prefix or chain.__class__.__name__

    return create_model(f"{prefix}Request", **request_fields)


def create_response_model(chain: Chain, prefix: str = None) -> BaseModel:
    """Create a pydantic response model for a LangChain instance.

    Args:
        chain: A LangChain instance.
        prefix: A prefix for the model name.
    """
    response_fields = {}

    for key in chain.output_keys:
        # TODO: add support for other output key types
        # based on demand
        if key == "source_documents":
            response_fields[key] = (list[Document], ...)
        else:
            response_fields[key] = (str, ...)

    prefix = prefix or chain.__class__.__name__

    return create_model(f"{prefix}Response", **response_fields)


def compile_model_prefix(path: str, chain: Chain) -> str:
    """Compile a prefix for pydantic models.

    Args:
        path: The path for the route.
        chain: A LangChain instance.
    """
    # Remove placeholders like '{item}' using regex
    path_wo_params = re.sub(r"\{.*?\}", "", path)
    path_prefix = "".join([part.capitalize() for part in path_wo_params.split("/")])

    chain_prefix = chain.__class__.__name__

    return f"{path_prefix}{chain_prefix}"


def get_streaming_callbacks(chain: Chain) -> list[Callable]:
    """Get streaming callbacks for a LangChain instance.

    Note: This function might not support all LangChain
    chain and agent types. Please open an issue on GitHub to
    request support for a specific type.

    Args:
        chain: A LangChain instance.
    """
    callbacks = []

    if "source_documents" in chain.output_keys:
        callbacks.append(SourceDocumentsStreamingCallbackHandler())

    if len(set(chain.output_keys) - {"source_documents"}) > 1:
        logger.warning(
            f"""multiple output keys found: {set(chain.output_keys) - {'source_documents'}}.

        Only the first output key will be used for streaming tokens. For more complex API logic, define the endpoint function manually.
        """
        )

    if isinstance(chain, AgentExecutor):
        callbacks.append(FinalTokenStreamingCallbackHandler())
    else:
        callbacks.extend(
            [
                TokenStreamingCallbackHandler(output_key=chain.output_keys[0]),
            ]
        )

    return callbacks


def get_websocket_callbacks(chain: Chain, websocket: WebSocket) -> list[Callable]:
    """Get websocket callbacks for a LangChain instance.

    Note: This function might not support all LangChain
    chain and agent types. Please open an issue on GitHub to
    request support for a specific type.

    Args:
        chain: A LangChain instance.
        websocket: A WebSocket instance.
    """
    callbacks = []

    if "source_documents" in chain.output_keys:
        callbacks.append(SourceDocumentsWebSocketCallbackHandler(websocket=websocket))

    if len(set(chain.output_keys) - {"source_documents"}) > 1:
        logger.warning(
            f"""multiple output keys found: {set(chain.output_keys) - {'source_documents'}}.

        Only the first output key will be used for sending tokens. For more complex websocket logic, define the endpoint function manually.
        """
        )

    if isinstance(chain, AgentExecutor):
        callbacks.append(FinalTokenWebSocketCallbackHandler(websocket=websocket))
    else:
        callbacks.extend(
            [
                TokenWebSocketCallbackHandler(
                    output_key=chain.output_keys[0], websocket=websocket
                ),
            ]
        )

    return callbacks
