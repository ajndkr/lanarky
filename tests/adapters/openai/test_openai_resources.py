from unittest.mock import AsyncMock, MagicMock

import pytest
from openai.types.chat import chat_completion, chat_completion_chunk

from lanarky.adapters.openai.resources import (
    AsyncOpenAI,
    ChatCompletion,
    ChatCompletionChunk,
    ChatCompletionResource,
    Message,
)


@pytest.mark.asyncio
async def test_chat_completion_resource_stream_response():
    async def mock_completion_chunk_stream():
        yield ChatCompletionChunk(
            id="chat-completion-id",
            created=1700936386,
            model="gpt-3.5-turbo-0613",
            object="chat.completion.chunk",
            choices=[
                chat_completion_chunk.Choice(
                    index=0,
                    finish_reason=None,
                    delta=chat_completion_chunk.ChoiceDelta(
                        content="Hello! How can I assist you today?"
                    ),
                )
            ],
        )

    chat_completion_resource = ChatCompletionResource(
        client=MagicMock(spec=AsyncOpenAI), stream=True
    )
    chat_completion_resource._client.chat = MagicMock()
    chat_completion_resource._client.chat.completions = MagicMock()
    chat_completion_resource._client.chat.completions.create = AsyncMock(
        return_value=mock_completion_chunk_stream()
    )

    messages = [Message(role="user", content="Hello")]
    async for response in chat_completion_resource.stream_response(messages):
        assert response == "Hello! How can I assist you today?"
        break

    chat_completion_resource = ChatCompletionResource(
        client=MagicMock(spec=AsyncOpenAI)
    )
    chat_completion_resource._client.chat = MagicMock()
    chat_completion_resource._client.chat.completions = MagicMock()
    chat_completion_resource._client.chat.completions.create = AsyncMock()
    chat_completion_resource._client.chat.completions.create.return_value = (
        ChatCompletion(
            id="chat-completion-id",
            created=1700936386,
            model="gpt-3.5-turbo-0613",
            object="chat.completion",
            choices=[
                chat_completion.Choice(
                    finish_reason="stop",
                    index=0,
                    message=chat_completion.ChatCompletionMessage(
                        content="Hello! How can I assist you today?", role="assistant"
                    ),
                )
            ],
        )
    )

    messages = [Message(role="user", content="Hello")]
    async for response in chat_completion_resource.stream_response(messages):
        assert response == "Hello! How can I assist you today?"
        break


@pytest.mark.asyncio
async def test_chat_completion_resource_call():
    mocked_completion = ChatCompletion(
        id="chat-completion-id",
        created=1700936386,
        model="gpt-3.5-turbo-0613",
        object="chat.completion",
        choices=[
            chat_completion.Choice(
                finish_reason="stop",
                index=0,
                message=chat_completion.ChatCompletionMessage(
                    content="Hello! How can I assist you today?", role="assistant"
                ),
            )
        ],
    )

    chat_completion_resource = ChatCompletionResource(
        client=MagicMock(spec=AsyncOpenAI)
    )
    chat_completion_resource._client.chat = MagicMock()
    chat_completion_resource._client.chat.completions = MagicMock()
    chat_completion_resource._client.chat.completions.create = AsyncMock(
        return_value=mocked_completion
    )

    messages = [Message(role="user", content="Hello")]
    response = await chat_completion_resource(messages)
    assert response == mocked_completion
