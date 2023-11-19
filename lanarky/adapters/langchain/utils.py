import re
from typing import Any, Callable

from fastapi import Depends
from langchain.agents import AgentExecutor
from langchain.chains.base import Chain
from langchain.schema.document import Document
from pydantic import BaseModel, create_model
from starlette.routing import compile_path

from lanarky.adapters.langchain.callbacks import (
    ChainStreamingCallbackHandler,
    FinalTokenStreamingCallbackHandler,
    SourceDocumentsStreamingCallbackHandler,
    TokenStreamingCallbackHandler,
)
from lanarky.adapters.langchain.responses import StreamingResponse
from lanarky.logging import logger


def build_factory_endpoint(
    path: str, endpoint: Callable[..., Any]
) -> Callable[..., Any]:
    try:
        chain = endpoint()
    except TypeError:
        raise TypeError("set default values for all factory endpoint parameters")

    if not isinstance(chain, Chain):
        raise TypeError("factory endpoint must return a Chain instance")

    # index 1 of `compile_path` contains path_format output
    model_prefix = compile_model_prefix(compile_path(path)[1], chain)

    request_model = create_request_model(path, model_prefix)
    callbacks = get_callbacks(chain)

    async def factory_endpoint(
        request: request_model, chain: Chain = Depends(endpoint)
    ):
        return StreamingResponse(
            chain=chain, config={"inputs": request.model_dump(), "callbacks": callbacks}
        )

    return factory_endpoint


def create_request_model(path: str, chain: Chain, prefix: str = "") -> BaseModel:
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
    # Remove placeholders like '{item}' using regex
    path_wo_params = re.sub(r"\{.*?\}", "", path)
    path_prefix = "".join([part.capitalize() for part in path_wo_params.split("/")])

    chain_prefix = chain.__class__.__name__

    return f"{path_prefix}{chain_prefix}"


def get_callbacks(chain: Chain) -> list[Callable]:
    callbacks = []

    if "source_documents" in chain.output_keys:
        callbacks.append(SourceDocumentsStreamingCallbackHandler())

    if len(set(chain.output_keys) - {"source_documents"}) > 1:
        logger.warning(
            f"""multiple output keys found: {set(chain.output_keys) - {'source_documents'}}.

        Only the first output key will be used for streaming. For more complex API logic, define the API endpoint logic manually.
        """
        )

    if isinstance(chain, AgentExecutor):
        callbacks.append(FinalTokenStreamingCallbackHandler())
    else:
        callbacks.extend(
            [
                TokenStreamingCallbackHandler(chain.output_keys[0]),
                ChainStreamingCallbackHandler(),
            ]
        )

    return callbacks
