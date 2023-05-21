from unittest.mock import AsyncMock

import pytest

from lanarky.callbacks.agents import (
    AsyncAgentsStreamingCallback,
    AsyncAgentsWebsocketCallback,
)


@pytest.mark.asyncio
async def test_check_if_answer_reached(send):
    callback = AsyncAgentsStreamingCallback(send=send)
    callback.last_tokens = ["", "", ""]
    callback.answer_reached = True

    serialized = {}
    prompts = []
    kwargs = {}

    await callback.on_llm_start(serialized, prompts, **kwargs)

    assert callback.last_tokens == ["", "", ""]
    assert callback.answer_reached is False

    token = "Final"

    result = callback._check_if_answer_reached(token)

    assert result is False
    assert callback.last_tokens == ["", "", "Final"]
    assert callback.answer_reached is False

    token = " Answer"

    result = callback._check_if_answer_reached(token)

    assert result is False
    assert callback.last_tokens == ["", "Final", " Answer"]
    assert callback.answer_reached is False

    token = ":"

    result = callback._check_if_answer_reached(token)

    assert result is None
    assert callback.last_tokens == ["Final", " Answer", ":"]
    assert callback.answer_reached is True


@pytest.mark.asyncio
async def test_async_agents_streaming_callback_on_llm_new_token_answer_not_reached(
    send: AsyncMock,
):
    callback = AsyncAgentsStreamingCallback(send=send)

    await callback.on_llm_new_token("\nFinal")
    callback.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_async_agents_websocket_callback_on_llm_new_token_answer_not_reached(
    websocket, bot_response
):
    callback = AsyncAgentsWebsocketCallback(websocket=websocket, response=bot_response)

    await callback.on_llm_new_token("\nFinal")

    callback.websocket.send_json.assert_not_awaited()
