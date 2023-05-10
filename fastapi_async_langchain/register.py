from typing import Any, Callable, Dict, List, Tuple


def register(key: str, _registry: Dict[str, Tuple[Any, List[str]]]) -> Any:
    """Add a class/function to a registry with required keyword arguments.

    ``_registry`` is a dictionary mapping from a key to a tuple of the class/function
    and a list of required keyword arguments, if keyword arguments are passed. Otherwise
    it is a dictionary mapping from a key to the class/function.
    """

    def _register_cls(cls: Any, required_kwargs: List = None) -> Any:
        if key in _registry:
            raise KeyError(f"{cls} already registered as {key}")
        _registry[key] = cls if required_kwargs is None else (cls, required_kwargs)
        return cls

    return _register_cls


STREAMING_CALLBACKS: Dict[str, Any] = {}
WEBSOCKET_CALLBACKS: Dict[str, Any] = {}


def register_streaming_callback(key: str) -> Callable:
    """Register an streaming callback handler."""

    def _register_cls(cls: Any) -> Callable:
        register(key, STREAMING_CALLBACKS)(cls=cls)
        return cls

    return _register_cls


def register_websocket_callback(key: str) -> Callable:
    """Register an websocket callback handler."""

    def _register_cls(cls: Any) -> Callable:
        register(key, WEBSOCKET_CALLBACKS)(cls=cls)
        return cls

    return _register_cls
