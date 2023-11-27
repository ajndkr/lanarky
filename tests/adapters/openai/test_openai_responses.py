from unittest.mock import AsyncMock, MagicMock, call

import pytest
from starlette.types import Send

from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.responses import (
    HTTPStatusDetail,
    StreamingResponse,
    status,
)
from lanarky.events import Events, ServerSentEvent, ensure_bytes


@pytest.mark.asyncio
async def test_stream_response_successful(send: Send):
    async def async_generator():
        yield ""

    resource = MagicMock(spec=ChatCompletionResource)
    resource.stream_response.__aiter__ = MagicMock(return_value=async_generator())

    response = StreamingResponse(
        resource=resource,
        messages=[],
    )

    await response.stream_response(send)

    resource.stream_response.assert_called_once()

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


@pytest.mark.asyncio
async def test_stream_response_error(send: Send):
    resource = MagicMock(spec=ChatCompletionResource)
    resource.stream_response = AsyncMock(side_effect=Exception("Some error occurred"))

    response = StreamingResponse(
        resource=resource,
        messages=[],
    )

    await response.stream_response(send)

    resource.stream_response.assert_called_once()

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
