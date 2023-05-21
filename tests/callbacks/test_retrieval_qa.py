from unittest.mock import MagicMock, call

import pytest

from lanarky.callbacks.retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)


@pytest.mark.asyncio
async def test_on_chain_end(send, websocket, bot_response):
    streaming_callback = AsyncBaseRetrievalQAStreamingCallback(send=send)
    outputs = {
        "source_documents": [
            MagicMock(page_content="Page 1 content", metadata={"source": "Source 1"}),
            MagicMock(page_content="Page 2 content", metadata={"source": "Source 2"}),
        ]
    }

    await streaming_callback.on_chain_end(outputs)

    streaming_callback.send.assert_has_calls(
        [
            call("\n\nSOURCE DOCUMENTS: \n"),
            call("\npage content: Page 1 content\nsource: Source 1\n"),
            call("\npage content: Page 2 content\nsource: Source 2\n"),
        ]
    )

    ws_callback = AsyncBaseRetrievalQAWebsocketCallback(
        websocket=websocket,
        response=bot_response,
    )
    await ws_callback.on_chain_end(outputs)

    ws_callback.websocket.send_json.assert_has_calls(
        [
            call({**bot_response.dict(), **{"message": "\n\nSOURCE DOCUMENTS: \n"}}),
            call(
                {
                    **bot_response.dict(),
                    **{"message": "\npage content: Page 1 content\nsource: Source 1\n"},
                }
            ),
            call(
                {
                    **bot_response.dict(),
                    **{"message": "\npage content: Page 2 content\nsource: Source 2\n"},
                }
            ),
        ]
    )
