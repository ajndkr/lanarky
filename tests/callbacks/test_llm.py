import pytest

from lanarky.callbacks.llm import (
    AsyncLLMChainStreamingCallback,
    AsyncLLMChainWebsocketCallback,
)


@pytest.mark.asyncio
async def test_async_llm_chain_streaming_callback_on_llm_new_token(send):
    callback = AsyncLLMChainStreamingCallback(send=send)

    await callback.on_llm_new_token("test_token")

    message = callback._construct_message("test_token")

    callback.send.assert_awaited_once_with(message)


@pytest.mark.asyncio
async def test_async_llm_chain_websocket_callback_on_llm_new_token(
    websocket, bot_response
):
    callback = AsyncLLMChainWebsocketCallback(
        websocket=websocket, response=bot_response
    )

    await callback.on_llm_new_token("test_token")

    message = callback._construct_message("test_token")

    callback.websocket.send_json.assert_awaited_once_with(message)
