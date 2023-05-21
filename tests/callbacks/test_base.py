from lanarky.callbacks.base import (
    AsyncStreamingResponseCallback,
    AsyncWebsocketCallback,
)


def test_always_verbose(send, websocket, bot_response):
    callback = AsyncStreamingResponseCallback(send=send)
    assert callback.always_verbose is True

    callback = AsyncWebsocketCallback(websocket=websocket, response=bot_response)
    assert callback.always_verbose is True
