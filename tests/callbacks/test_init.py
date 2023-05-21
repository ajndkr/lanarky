from unittest.mock import Mock

from langchain.chains import LLMChain

from lanarky.callbacks import (
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainWebsocketCallback,
    get_streaming_callback,
    get_websocket_callback,
)


def test_get_streaming_callback():
    chain = Mock(spec=LLMChain)
    callback = get_streaming_callback(chain)
    assert isinstance(callback, AsyncLLMChainStreamingCallback)


def test_get_websocket_callback():
    chain = Mock(spec=LLMChain)
    callback = get_websocket_callback(chain)
    assert isinstance(callback, AsyncLLMChainWebsocketCallback)
