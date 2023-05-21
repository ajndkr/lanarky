from unittest.mock import MagicMock, call

import pytest

from lanarky.callbacks.retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)


@pytest.fixture
def outputs():
    return {
        "source_documents": [
            MagicMock(page_content="Page 1 content", metadata={"source": "Source 1"}),
            MagicMock(page_content="Page 2 content", metadata={"source": "Source 2"}),
        ]
    }


@pytest.fixture
def messages():
    return [
        "\n\nSOURCE DOCUMENTS: \n",
        "\npage content: Page 1 content\nsource: Source 1\n",
        "\npage content: Page 2 content\nsource: Source 2\n",
    ]


@pytest.mark.asyncio
async def test_streaming_on_chain_end(send, outputs, messages):
    callback = AsyncBaseRetrievalQAStreamingCallback(send=send)

    await callback.on_chain_end(outputs)

    callback.send.assert_has_calls(
        [call(callback._construct_message(message)) for message in messages]
    )


@pytest.mark.asyncio
async def test_websocket_on_chain_end(websocket, bot_response, outputs, messages):
    ws_callback = AsyncBaseRetrievalQAWebsocketCallback(
        websocket=websocket,
        response=bot_response,
    )
    await ws_callback.on_chain_end(outputs)

    ws_callback.websocket.send_json.assert_has_calls(
        [call(ws_callback._construct_message(message)) for message in messages]
    )
