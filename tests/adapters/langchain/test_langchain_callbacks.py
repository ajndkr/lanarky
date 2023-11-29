from unittest.mock import MagicMock, create_autospec, patch

import pytest
from langchain.agents import AgentExecutor
from langchain.chains import ConversationChain
from langchain.schema.document import Document
from starlette.types import Send

from lanarky.adapters.langchain import callbacks
from lanarky.adapters.langchain.utils import (
    get_streaming_callbacks,
    get_websocket_callbacks,
)
from lanarky.websockets import WebSocket


def test_always_verbose():
    callback = callbacks.LanarkyCallbackHandler()
    assert callback.always_verbose is True


def test_llm_cache_used():
    callback = callbacks.LanarkyCallbackHandler()
    assert callback.llm_cache_used is False

    with patch("lanarky.adapters.langchain.callbacks.get_llm_cache") as get_llm_cache:
        from langchain.cache import InMemoryCache

        get_llm_cache.return_value = InMemoryCache()

        callback = callbacks.LanarkyCallbackHandler()
        assert callback.llm_cache_used is True


def test_streaming_callback(send: Send):
    callback = callbacks.StreamingCallbackHandler()

    assert callback.send is None

    callback.send = send
    assert callback.send == send

    with pytest.raises(ValueError):
        callback.send = "non_callable_value"


def test_websocket_callback(websocket: WebSocket):
    callback = callbacks.WebSocketCallbackHandler()

    assert callback.websocket is None

    callback.websocket = websocket
    assert callback.websocket == websocket

    with pytest.raises(ValueError):
        callback.websocket = "non_websocket_value"


def test_callbacks_construct_message():
    callback = callbacks.StreamingCallbackHandler()

    with patch("lanarky.adapters.langchain.callbacks.ServerSentEvent") as sse, patch(
        "lanarky.adapters.langchain.callbacks.ensure_bytes"
    ) as ensure_bytes:
        data = "test_data"
        event = "test_event"
        expected_return_value = {
            "type": "http.response.body",
            "body": ensure_bytes.return_value,
            "more_body": True,
        }

        result = callback._construct_message(data, event)

        sse.assert_called_with(data=data, event=event)
        ensure_bytes.assert_called_with(sse.return_value, None)

        assert result == expected_return_value

    callback = callbacks.WebSocketCallbackHandler()

    data = "test_data"
    event = "test_event"

    expected_return_value = dict(data=data, event=event)

    assert callback._construct_message(data, event) == expected_return_value


def test_get_token():
    with pytest.raises(ValueError):
        callbacks.get_token_data(token="test_token", mode="wrong_mode")

    assert callbacks.get_token_data(token="test_token", mode="text") == "test_token"
    assert (
        callbacks.get_token_data(token="test_token", mode="json")
        == '{"token":"test_token"}'
    )


@pytest.mark.asyncio
async def test_token_callbacks(send: Send, websocket: WebSocket):
    with pytest.raises(ValueError):
        callbacks.TokenStreamingCallbackHandler(mode="wrong_mode", output_key="dummy")

    callback = callbacks.TokenStreamingCallbackHandler(send=send, output_key="dummy")

    await callback.on_chain_start()
    assert not callback.streaming

    await callback.on_llm_new_token("test_token")
    assert callback.streaming
    assert not callback.llm_cache_used
    callback.send.assert_awaited()

    callback.llm_cache_used = True
    await callback.on_llm_new_token("test_token")
    assert not callback.llm_cache_used

    send.reset_mock()
    callback = callbacks.TokenStreamingCallbackHandler(send=send, output_key="dummy")
    outputs = {"dummy": "output_data"}
    await callback.on_chain_end(outputs)
    callback.send.assert_awaited()

    send.reset_mock()
    callback = callbacks.TokenStreamingCallbackHandler(send=send, output_key="dummy")
    callback.llm_cache_used = False
    callback.streaming = True
    await callback.on_chain_end(outputs)
    callback.send.assert_not_awaited()

    send.reset_mock()
    callback = callbacks.TokenStreamingCallbackHandler(send=send, output_key="dummy")
    callback.streaming = False
    with pytest.raises(KeyError):
        await callback.on_chain_end({"wrong_key": "output_data"})

    with pytest.raises(ValueError):
        callbacks.TokenWebSocketCallbackHandler(mode="wrong_mode", output_key="dummy")

    callback = callbacks.TokenWebSocketCallbackHandler(
        websocket=websocket, output_key="dummy"
    )

    await callback.on_chain_start()
    assert not callback.streaming

    await callback.on_llm_new_token("test_token")
    assert callback.streaming
    assert not callback.llm_cache_used
    callback.websocket.send_json.assert_awaited()

    callback.llm_cache_used = True
    await callback.on_llm_new_token("test_token")
    assert not callback.llm_cache_used

    websocket.send_json.reset_mock()
    callback = callbacks.TokenWebSocketCallbackHandler(
        websocket=websocket, output_key="dummy"
    )
    outputs = {"dummy": "output_data"}
    await callback.on_chain_end(outputs)
    callback.websocket.send_json.assert_awaited()

    websocket.send_json.reset_mock()
    callback = callbacks.TokenWebSocketCallbackHandler(
        websocket=websocket, output_key="dummy"
    )
    callback.llm_cache_used = False
    callback.streaming = True
    await callback.on_chain_end(outputs)
    callback.websocket.send_json.assert_not_awaited()

    websocket.send_json.reset_mock()
    callback = callbacks.TokenWebSocketCallbackHandler(
        websocket=websocket, output_key="dummy"
    )
    callback.streaming = False
    with pytest.raises(KeyError):
        await callback.on_chain_end({"wrong_key": "output_data"})


@pytest.mark.asyncio
async def test_source_documents_callbacks(send: Send, websocket: WebSocket):
    callback = callbacks.SourceDocumentsStreamingCallbackHandler(send=send)

    outputs = {"source_documents": "output_data"}
    with pytest.raises(ValueError):
        await callback.on_chain_end(outputs)

    outputs = {"source_documents": ["output_data"]}
    with pytest.raises(ValueError):
        await callback.on_chain_end(outputs)

    outputs = {"source_documents": [Document(page_content="test_content")]}
    await callback.on_chain_end(outputs)
    callback.send.assert_awaited()

    send.reset_mock()
    outputs = {"dummy": "output_data"}
    await callback.on_chain_end(outputs)
    callback.send.assert_not_awaited()

    callback = callbacks.SourceDocumentsWebSocketCallbackHandler(websocket=websocket)

    outputs = {"source_documents": "output_data"}
    with pytest.raises(ValueError):
        await callback.on_chain_end(outputs)

    outputs = {"source_documents": ["output_data"]}
    with pytest.raises(ValueError):
        await callback.on_chain_end(outputs)

    outputs = {"source_documents": [Document(page_content="test_content")]}
    await callback.on_chain_end(outputs)
    callback.websocket.send_json.assert_awaited()

    websocket.send_json.reset_mock()
    outputs = {"dummy": "output_data"}
    await callback.on_chain_end(outputs)
    callback.websocket.send_json.assert_not_awaited()


@pytest.mark.asyncio
async def test_final_token_callbacks(send: Send, websocket: WebSocket):
    callback = callbacks.FinalTokenStreamingCallbackHandler(
        send=send, stream_prefix=True
    )

    await callback.on_llm_start()
    assert not callback.answer_reached
    assert not callback.streaming

    await callback.on_llm_new_token("test_token")
    assert callback.streaming

    callback.check_if_answer_reached = MagicMock(return_value=True)
    await callback.on_llm_new_token("test_token")
    assert callback.answer_reached
    callback.send.assert_awaited()

    send.reset_mock()
    callback = callbacks.FinalTokenStreamingCallbackHandler(
        send=send, stream_prefix=True
    )
    callback.check_if_answer_reached = MagicMock(return_value=False)
    await callback.on_llm_new_token("test_token")
    assert not callback.answer_reached
    callback.send.assert_not_awaited()

    callback = callbacks.FinalTokenWebSocketCallbackHandler(
        websocket=websocket, stream_prefix=True
    )

    await callback.on_llm_start()
    assert not callback.answer_reached
    assert not callback.streaming

    await callback.on_llm_new_token("test_token")
    assert callback.streaming

    callback.check_if_answer_reached = MagicMock(return_value=True)
    await callback.on_llm_new_token("test_token")
    assert callback.answer_reached
    callback.websocket.send_json.assert_awaited()

    websocket.send_json.reset_mock()
    callback = callbacks.FinalTokenWebSocketCallbackHandler(
        websocket=websocket, stream_prefix=True
    )
    callback.check_if_answer_reached = MagicMock(return_value=False)
    await callback.on_llm_new_token("test_token")
    assert not callback.answer_reached
    callback.websocket.send_json.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_callbacks(websocket: WebSocket):
    def chain_factory():
        chain: ConversationChain = create_autospec(ConversationChain)
        chain.input_keys = ["input"]
        chain.output_keys = ["response", "source_documents"]
        return chain

    streaming_callbacks = get_streaming_callbacks(chain_factory())
    assert len(streaming_callbacks) == 2

    def agent_factory():
        agent: AgentExecutor = create_autospec(AgentExecutor)
        return agent

    websocket_callbacks = get_streaming_callbacks(agent_factory())
    assert len(websocket_callbacks) == 1

    websocket_callbacks = get_websocket_callbacks(chain_factory(), websocket)
    assert len(websocket_callbacks) == 2

    websocket_callbacks = get_websocket_callbacks(agent_factory(), websocket)
    assert len(websocket_callbacks) == 1
