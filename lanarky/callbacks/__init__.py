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
    chain: Chain, *args, **kwargs
) -> AsyncStreamingResponseCallback:
    """Get the streaming callback for the given chain type."""
    chain_type = chain.__class__.__name__
    try:
        callback = STREAMING_CALLBACKS[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type,
                callable_name="AsyncStreamingResponseCallback",
                chain_types="\n".join(list(STREAMING_CALLBACKS.keys())),
            )
        )


def get_websocket_callback(chain: Chain, *args, **kwargs) -> AsyncWebsocketCallback:
    """Get the websocket callback for the given chain type."""
    chain_type = chain.__class__.__name__
    try:
        callback = WEBSOCKET_CALLBACKS[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type,
                callable_name="AsyncWebsocketCallback",
                chain_types="\n".join(list(WEBSOCKET_CALLBACKS.keys())),
            )
        )


def get_streaming_json_callback(
    chain: Chain, *args, **kwargs
) -> AsyncStreamingJSONResponseCallback:
    """Get the streaming JSON callback for the given chain type."""
    chain_type = chain.__class__.__name__
    try:
        callback = STREAMING_JSON_CALLBACKS[chain_type]
        return callback(*args, **kwargs)
    except KeyError:
        raise KeyError(
            ERROR_MESSAGE.format(
                chain_type=chain_type,
                callable_name="AsyncStreamingJSONResponseCallback",
                chain_types="\n".join(list(STREAMING_JSON_CALLBACKS.keys())),
            )
        )
