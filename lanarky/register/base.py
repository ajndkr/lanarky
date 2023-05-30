from typing import Any, Optional, Union


def register(
    key: Union[list[str], str],
    _registry: dict[str, tuple[Any, list[str]]],
    *,
    override: bool = False,
) -> Any:
    """Add a class/function to a registry with required keyword arguments.

    ``_registry`` is a dictionary mapping from a key to a tuple of the class/function
    and a list of required keyword arguments, if keyword arguments are passed. Otherwise
    it is a dictionary mapping from a key to the class/function.

    Args:
        key: key or list of keys to register the class/function under.
        _registry: registry to add the class/function to.
        override: if True, override existing keys in the registry.
    """

    def _register_cls(cls: Any, required_kwargs: Optional[list] = None) -> Any:
        if isinstance(key, str):
            keys = [key]
        else:
            keys = key

        for _key in keys:
            if _key in _registry and not override:
                raise KeyError(f"{cls} already registered as {_key}")
            _registry[_key] = cls if required_kwargs is None else (cls, required_kwargs)
        return cls

    return _register_cls
