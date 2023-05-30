from typing import Any, Dict, List, Tuple

import pytest

from lanarky.register import (
    STREAMING_CALLBACKS,
    STREAMING_JSON_CALLBACKS,
    WEBSOCKET_CALLBACKS,
    register_streaming_callback,
    register_streaming_json_callback,
    register_websocket_callback,
)
from lanarky.register.base import register


@pytest.fixture
def registry() -> Dict[str, Tuple[Any, List[str]]]:
    return {}


def test_register(registry: Dict[str, Tuple[Any, List[str]]]):
    class MyClass:
        pass

    register("my_key", registry)(cls=MyClass)
    assert registry["my_key"] == MyClass

    with pytest.raises(KeyError):
        register("my_key", registry)(cls=MyClass)

    class MyOtherClass:
        pass

    register("my_key", registry, override=True)(cls=MyOtherClass)
    assert registry["my_key"] == MyOtherClass


def test_register_with_required_kwargs(registry: Dict[str, Tuple[Any, List[str]]]):
    class MyClass:
        pass

    register("my_key", registry)(cls=MyClass, required_kwargs=["arg1", "arg2"])

    assert isinstance(registry["my_key"], tuple)
    assert registry["my_key"][0] == MyClass
    assert registry["my_key"][1] == ["arg1", "arg2"]


def test_register_streaming_callback(registry: Dict[str, Tuple[Any, List[str]]]):
    class MyStreamingCallback:
        pass

    register_streaming_callback("my_streaming_callback")(cls=MyStreamingCallback)
    assert "my_streaming_callback" in STREAMING_CALLBACKS
    assert STREAMING_CALLBACKS["my_streaming_callback"] == MyStreamingCallback

    with pytest.raises(KeyError):
        register_streaming_callback("my_streaming_callback")(cls=MyStreamingCallback)

    class MyOtherStreamingCallback:
        pass

    register_streaming_callback("my_streaming_callback", override=True)(
        cls=MyOtherStreamingCallback
    )
    assert STREAMING_CALLBACKS["my_streaming_callback"] == MyOtherStreamingCallback


def test_register_websocket_callback(registry: Dict[str, Tuple[Any, List[str]]]):
    class MyWebsocketCallback:
        pass

    register_websocket_callback("my_websocket_callback")(cls=MyWebsocketCallback)
    assert "my_websocket_callback" in WEBSOCKET_CALLBACKS
    assert WEBSOCKET_CALLBACKS["my_websocket_callback"] == MyWebsocketCallback

    with pytest.raises(KeyError):
        register_websocket_callback("my_websocket_callback")(cls=MyWebsocketCallback)

    class MyOtherWebsocketCallback:
        pass

    register_websocket_callback("my_websocket_callback", override=True)(
        cls=MyOtherWebsocketCallback
    )

    assert WEBSOCKET_CALLBACKS["my_websocket_callback"] == MyOtherWebsocketCallback


def test_register_streaming_json_callback(registry: Dict[str, Tuple[Any, List[str]]]):
    class MyStreamingJsonCallback:
        pass

    register_streaming_json_callback("my_streaming_json_callback")(
        cls=MyStreamingJsonCallback
    )
    assert (
        STREAMING_JSON_CALLBACKS["my_streaming_json_callback"]
        == MyStreamingJsonCallback
    )

    with pytest.raises(KeyError):
        register_streaming_json_callback("my_streaming_json_callback")(
            cls=MyStreamingJsonCallback
        )

    class MyOtherStreamingJsonCallback:
        pass

    register_streaming_json_callback("my_streaming_json_callback", override=True)(
        cls=MyOtherStreamingJsonCallback
    )
    assert (
        STREAMING_JSON_CALLBACKS["my_streaming_json_callback"]
        == MyOtherStreamingJsonCallback
    )
