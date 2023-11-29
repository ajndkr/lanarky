from typing import Type
from unittest.mock import AsyncMock, MagicMock, call

import pytest
from langchain.chains.base import Chain
from starlette.background import BackgroundTask
from starlette.types import Send

from lanarky.adapters.langchain.callbacks import TokenStreamingCallbackHandler
from lanarky.adapters.langchain.responses import (
    HTTPStatusDetail,
    StreamingResponse,
    status,
)
from lanarky.events import Events, ServerSentEvent, ensure_bytes


@pytest.fixture
def chain() -> Type[Chain]:
    return MagicMock(spec=Chain)


@pytest.mark.asyncio
async def test_stream_response_successful(send: Send, chain: Type[Chain]):
    response = StreamingResponse(
        chain=chain,
        config={"callbacks": [TokenStreamingCallbackHandler(output_key="dummy")]},
        background=BackgroundTask(lambda: None),
    )

    chain.acall = AsyncMock(return_value={})

    await response.stream_response(send)

    chain.acall.assert_called_once()

    expected_calls = [
        call(
            {
                "type": "http.response.start",
                "status": response.status_code,
                "headers": response.raw_headers,
            }
        ),
        call(
            {
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            }
        ),
    ]

    send.assert_has_calls(expected_calls, any_order=False)

    assert "outputs" in response.background.kwargs


@pytest.mark.asyncio
async def test_stream_response_error(send: Send, chain: Type[Chain]):
    response = StreamingResponse(
        chain=chain,
        config={"callbacks": []},
        background=BackgroundTask(lambda: None),
    )

    chain.acall = AsyncMock(side_effect=Exception("Some error occurred"))

    await response.stream_response(send)

    chain.acall.assert_called_once()

    expected_calls = [
        call(
            {
                "type": "http.response.start",
                "status": response.status_code,
                "headers": response.raw_headers,
            }
        ),
        call(
            {
                "type": "http.response.body",
                "body": ensure_bytes(
                    ServerSentEvent(
                        data=dict(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=HTTPStatusDetail.INTERNAL_SERVER_ERROR,
                        ),
                        event=Events.ERROR,
                    ),
                    None,
                ),
                "more_body": True,
            }
        ),
        call(
            {
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            }
        ),
    ]

    send.assert_has_calls(expected_calls, any_order=False)

    assert "error" in response.background.kwargs
