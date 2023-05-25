from typing import Any, Optional

from langchain.chains.base import Chain

from lanarky.register import (
    STREAMING_CALLBACKS,
    STREAMING_JSON_CALLBACKS,
    WEBSOCKET_CALLBACKS,
)

from .agents import *  # noqa: F401, F403
from .base import (
    AsyncStreamingJSONResponseCallback,
    AsyncStreamingResponseCallback,
    AsyncWebsocketCallback,
)
from .llm import *  # noqa: F401, F403
from .retrieval_qa import *  # noqa: F401, F403

ERROR_MESSAGE = """Error! Chain type '{chain_type}' is not currently supported by '{callable_name}'.
Available chain types: {chain_types}

To use a custom chain type, you must register a new callback handler.
See the documentation for more details: https://lanarky.readthedocs.io/en/latest/advanced/custom_callbacks.html
"""


def get_streaming_callback(
    chain: Chain, override: Optional[str] = None, *args, **kwargs
) -> AsyncStreamingResponseCallback:
    """Get the streaming callback for the given chain type."""
    return _get_callback(
        chain,
        override,
        STREAMING_CALLBACKS,
        "AsyncStreamingResponseCallback",
        *args,
        **kwargs
    )


def get_websocket_callback(
    chain: Chain, override: Optional[str] = None, *args, **kwargs
) -> AsyncWebsocketCallback:
    """Get the websocket callback for the given chain type."""
    return _get_callback(
        chain, override, WEBSOCKET_CALLBACKS, "AsyncWebsocketCallback", *args, **kwargs
    )


def get_streaming_json_callback(
    chain: Chain, override: Optional[str] = None, *args, **kwargs
) -> AsyncStreamingJSONResponseCallback:
    """Get the streaming JSON callback for the given chain type."""
    return _get_callback(
        chain,
        override,
        STREAMING_JSON_CALLBACKS,
        "AsyncStreamingJSONResponseCallback",
        *args,
        **kwargs
    )


def _get_callback(
    chain: Chain,
    override: Optional[str],
    callback_registry: dict[str, Any],
    callable_name: str,
    *args,
    **kwargs
):
    """Base function for getting a callback from a registry.

    Args:
        chain: The chain to get the callback for.
        override: The name of the chain type to use instead of the chain's type.
        callback_registry: The registry to get the callback from.
        callable_name: The name of the callable to use in the error message.
        *args: Positional arguments to pass to the callback.
        **kwargs: Keyword arguments to pass to the callback.
    """
    chain_type = override or chain.__class__.__name__
    try:
        callback = callback_registry[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type,
                callable_name=callable_name,
                chain_types="\n".join(list(callback_registry.keys())),
            )
        )
