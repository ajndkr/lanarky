from unittest.mock import MagicMock, call

import pytest

from lanarky.callbacks.retrieval_qa import (
    AsyncBaseRetrievalQAStreamingCallback,
    AsyncBaseRetrievalQAStreamingJSONCallback,
    AsyncBaseRetrievalQAWebsocketCallback,
)
from lanarky.schemas import (
    AnswerStreamingJSONResponse,
    BaseRetrievalQAStreamingJSONResponse,
)


@pytest.fixture
def outputs():
    return {
        "answer": "Answer for when LLM cache is enabled.",
        "source_documents": [
            MagicMock(page_content="Page 1 content", metadata={"source": "Source 1"}),
            MagicMock(page_content="Page 2 content", metadata={"source": "Source 2"}),
        ],
    }


@pytest.fixture
def messages():
    return [
        "\n\nSOURCE DOCUMENTS:\n",
        "\npage content: Page 1 content\nsource: Source 1\n",
        "\npage content: Page 2 content\nsource: Source 2\n",
    ]


@pytest.mark.asyncio
async def test_streaming_on_chain_end(send, outputs, messages):
    import langchain

    langchain.llm_cache = None

    callback = AsyncBaseRetrievalQAStreamingCallback(send=send)

    await callback.on_chain_end(outputs)

    callback.send.assert_has_calls(
        [call(callback._construct_message(message)) for message in messages]
    )


@pytest.mark.asyncio
async def test_streaming_on_chain_end_cache_enabled(send, outputs, messages):
    import langchain
    from langchain.cache import InMemoryCache

    langchain.llm_cache = InMemoryCache()

    callback = AsyncBaseRetrievalQAStreamingCallback(send=send)

    await callback.on_chain_end(outputs)

    if callback.llm_cache_used:
        callback.send.assert_has_calls(
            [call(callback._construct_message(outputs["answer"]))]
        )

    callback.send.assert_has_calls(
        [call(callback._construct_message(message)) for message in messages]
    )


@pytest.mark.asyncio
async def test_websocket_on_chain_end(websocket, bot_response, outputs, messages):
    import langchain

    langchain.llm_cache = None

    callback = AsyncBaseRetrievalQAWebsocketCallback(
        websocket=websocket,
        response=bot_response,
    )
    await callback.on_chain_end(outputs)

    callback.websocket.send_json.assert_has_calls(
        [call(callback._construct_message(message)) for message in messages]
    )


@pytest.mark.asyncio
async def test_websocket_on_chain_end_cache_enabled(
    websocket, bot_response, outputs, messages
):
    import langchain
    from langchain.cache import InMemoryCache

    langchain.llm_cache = InMemoryCache()

    callback = AsyncBaseRetrievalQAWebsocketCallback(
        websocket=websocket,
        response=bot_response,
    )
    await callback.on_chain_end(outputs)

    if callback.llm_cache_used:
        callback.websocket.send_json.assert_has_calls(
            [call(callback._construct_message(outputs["answer"]))]
        )

    callback.websocket.send_json.assert_has_calls(
        [call(callback._construct_message(message)) for message in messages]
    )


@pytest.mark.asyncio
async def test_streaming_json_on_chain_end(send, outputs):
    import langchain

    langchain.llm_cache = None

    callback = AsyncBaseRetrievalQAStreamingJSONCallback(send=send)

    await callback.on_chain_end(outputs)

    source_documents = [document.dict() for document in outputs["source_documents"]]

    callback.send.assert_awaited_once_with(
        callback._construct_message(
            BaseRetrievalQAStreamingJSONResponse(source_documents=source_documents)
        )
    )


@pytest.mark.asyncio
async def test_streaming_json_on_chain_end_cache_enabled(send, outputs):
    import langchain
    from langchain.cache import InMemoryCache

    langchain.llm_cache = InMemoryCache()

    callback = AsyncBaseRetrievalQAStreamingJSONCallback(send=send)

    await callback.on_chain_end(outputs)

    source_documents = [document.dict() for document in outputs["source_documents"]]
    answer = outputs["answer"]

    awaits_expected = []
    if callback.llm_cache_used:
        awaits_expected.append(
            call(
                callback._construct_message(AnswerStreamingJSONResponse(answer=answer))
            )
        )

    awaits_expected.append(
        call(
            callback._construct_message(
                BaseRetrievalQAStreamingJSONResponse(source_documents=source_documents)
            )
        )
    )

    callback.send.assert_has_awaits(awaits_expected)
