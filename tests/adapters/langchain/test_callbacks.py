from typing import Type
from unittest.mock import AsyncMock, patch

import pytest
from starlette.types import Send

from lanarky.adapters.langchain import callbacks


def test_always_verbose():
    callback = callbacks.LanarkyCallbackHandler()
    assert callback.always_verbose is True


def test_llm_cache_used():
    callback = callbacks.LanarkyCallbackHandler()
    assert callback.llm_cache_used is False

    from langchain.cache import InMemoryCache
    from langchain.globals import set_llm_cache

    set_llm_cache(InMemoryCache())

    callback = callbacks.LanarkyCallbackHandler()
    assert callback.llm_cache_used is True


def test_streaming_callback_send(send: Send):
    callback = callbacks.StreamingCallbackHandler()

    assert callback.send is None

    callback.send = send
    assert callback.send == send

    with pytest.raises(ValueError):
        callback.send = "non_callable_value"


def ttest_streaming_callback_construct_message():
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


@pytest.mark.asyncio
async def test_chain_streaming(send: Send):
    callback = callbacks.ChainStreamingCallbackHandler(send=send)

    await callback.on_llm_start()

    callback.send.assert_awaited()

    await callback.on_chain_end()

    callback.send.assert_awaited()


@pytest.fixture
def token_streaming_callback(
    send: Send,
) -> Type[callbacks.TokenStreamingCallbackHandler]:
    return callbacks.TokenStreamingCallbackHandler(
        send=send, output_key="output_key_test", mode=callbacks.TokenStreamMode.JSON
    )


@pytest.mark.asyncio
async def test_token_streaming_callback_on_chain_start(
    token_streaming_callback: Type[callbacks.TokenStreamingCallbackHandler],
):
    await token_streaming_callback.on_chain_start()
    assert not token_streaming_callback.streaming


@pytest.mark.asyncio
async def test_token_streaming_callback_on_llm_new_token(
    token_streaming_callback: Type[callbacks.TokenStreamingCallbackHandler],
):
    token_streaming_callback.streaming = True
    token_streaming_callback.llm_cache_used = True

    await token_streaming_callback.on_llm_new_token("test_token")
    assert token_streaming_callback.streaming
    assert (
        not token_streaming_callback.llm_cache_used
    )  # Check that llm_cache_used is set to False

    token_streaming_callback._construct_message = AsyncMock()

    await token_streaming_callback.on_llm_new_token("another_test_token")

    expected_data = callbacks.get_token_data(
        token="another_test_token", mode=token_streaming_callback.mode
    )
    token_streaming_callback._construct_message.assert_called_with(
        data=expected_data, event=callbacks.Events.COMPLETION
    )


@pytest.mark.asyncio
async def test_token_streaming_callback_on_chain_end(
    token_streaming_callback: Type[callbacks.TokenStreamingCallbackHandler],
):
    token_streaming_callback.streaming = True
    token_streaming_callback.llm_cache_used = True

    outputs = {"output_key_test": "output_data"}

    token_streaming_callback._construct_message = AsyncMock()

    await token_streaming_callback.on_chain_end(outputs)

    expected_data = callbacks.get_token_data(
        token="output_data", mode=token_streaming_callback.mode
    )

    token_streaming_callback._construct_message.assert_called_with(
        data=expected_data, event=callbacks.Events.COMPLETION
    )
    token_streaming_callback.send.assert_awaited()

    token_streaming_callback.output_key = "non_existing_key"
    with pytest.raises(KeyError):
        await token_streaming_callback.on_chain_end(outputs)
