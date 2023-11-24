from typing import Iterator, Type
from unittest.mock import MagicMock, call

import pytest
from fastapi import status
from starlette.types import Send

from lanarky.events import Events, ServerSentEvent, ensure_bytes
from lanarky.responses import HTTPStatusDetail, StreamingResponse


@pytest.fixture
def streaming_response(body_iterator: Iterator[bytes]) -> Type[StreamingResponse]:
    return StreamingResponse(content=body_iterator)


@pytest.mark.asyncio
async def test_stream_response_successful(
    send: Send, streaming_response: Type[StreamingResponse]
):
    await streaming_response.stream_response(send)

    expected_calls = [
        call(
            {
                "type": "http.response.start",
                "status": streaming_response.status_code,
                "headers": streaming_response.raw_headers,
            }
        ),
        call(
            {
                "type": "http.response.body",
                "body": b"Chunk 1",
                "more_body": True,
            }
        ),
        call(
            {
                "type": "http.response.body",
                "body": b"Chunk 2",
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


@pytest.mark.asyncio
async def test_stream_response_exception(
    send: Send, streaming_response: Type[StreamingResponse]
):
    streaming_response.body_iterator = MagicMock()
    streaming_response.body_iterator.__aiter__.side_effect = Exception("Some error")

    await streaming_response.stream_response(send)

    expected_calls = [
        call(
            {
                "type": "http.response.start",
                "status": streaming_response.status_code,
                "headers": streaming_response.raw_headers,
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
