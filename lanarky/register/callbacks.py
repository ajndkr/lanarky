from typing import Any, Callable, Union

from .base import register

STREAMING_CALLBACKS: dict[str, Any] = {}
WEBSOCKET_CALLBACKS: dict[str, Any] = {}
STREAMING_JSON_CALLBACKS: dict[str, Any] = {}


def register_streaming_callback(key: Union[list[str], str], **kwargs) -> Callable:
    """Register a streaming callback handler."""

    def _register_cls(cls: Any) -> Callable:
        register(key, STREAMING_CALLBACKS, **kwargs)(cls=cls)
        return cls

    return _register_cls


def register_websocket_callback(key: Union[list[str], str], **kwargs) -> Callable:
    """Register a websocket callback handler."""

    def _register_cls(cls: Any) -> Callable:
        register(key, WEBSOCKET_CALLBACKS, **kwargs)(cls=cls)
        return cls

    return _register_cls


def register_streaming_json_callback(key: Union[list[str], str], **kwargs) -> Callable:
    """Register an streaming json callback handler."""

    def _register_cls(cls: Any) -> Callable:
        register(key, STREAMING_JSON_CALLBACKS, **kwargs)(cls=cls)
        return cls

    return _register_cls
