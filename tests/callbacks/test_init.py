from unittest.mock import Mock

import pytest
from langchain.chains import LLMChain

from lanarky.callbacks import (
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainWebsocketCallback,
    get_streaming_callback,
    get_websocket_callback,
)


def test_get_streaming_callback(send):
    chain = Mock(spec=LLMChain)
    callback = get_streaming_callback(chain, send=send)
    assert isinstance(callback, AsyncLLMChainStreamingCallback)

    with pytest.raises(KeyError):

        class CustomChain:
            pass

        chain = Mock(spec=CustomChain)
        get_streaming_callback(chain, send=send)


def test_get_websocket_callback(websocket, bot_response):
    chain = Mock(spec=LLMChain)
    callback = get_websocket_callback(chain, websocket=websocket, response=bot_response)
    assert isinstance(callback, AsyncLLMChainWebsocketCallback)

    with pytest.raises(KeyError):

        class CustomChain:
            pass

        chain = Mock(spec=CustomChain)
        get_websocket_callback(chain, websocket=websocket, response=bot_response)
