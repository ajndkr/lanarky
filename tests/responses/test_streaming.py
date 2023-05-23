from unittest.mock import AsyncMock, MagicMock

import pytest
from starlette.background import BackgroundTask

from lanarky.callbacks import get_streaming_callback, get_streaming_json_callback
from lanarky.responses import StreamingResponse


@pytest.fixture
def inputs() -> dict[str, str]:
    return {"input": "data"}


@pytest.fixture
def background() -> BackgroundTask:
    return BackgroundTask(lambda: None)


@pytest.fixture
def streaming_response(
    chain: MagicMock, inputs: dict[str, str], background: BackgroundTask
) -> StreamingResponse:
    return StreamingResponse.from_chain(
        chain=chain, inputs=inputs, background=background
    )


def test_init_from_chain(streaming_response: StreamingResponse) -> None:
    assert isinstance(streaming_response, StreamingResponse)
    assert streaming_response.chain_executor is not None
    assert isinstance(streaming_response.background, BackgroundTask)


@pytest.mark.asyncio
async def test_streaming_create_chain_executor(
    chain: MagicMock, inputs: dict[str, str], send
) -> None:
    chain_executor = StreamingResponse._create_chain_executor(
        chain=chain, inputs=inputs
    )

    assert callable(chain_executor)

    chain.acall.assert_not_called()

    await chain_executor(send)

    chain.acall.assert_called_once_with(
        inputs=inputs, callbacks=[get_streaming_callback(chain=chain, send=send)]
    )


@pytest.mark.asyncio
async def test_stream_response(
    streaming_response: StreamingResponse, send: AsyncMock, chain: MagicMock
):
    await streaming_response.stream_response(send=send)

    send.assert_any_call(
        {
            "type": "http.response.start",
            "status": streaming_response.status_code,
            "headers": streaming_response.raw_headers,
        }
    )

    send.assert_any_call(
        {"type": "http.response.body", "body": b"", "more_body": False}
    )


@pytest.mark.asyncio
async def test_stream_response_error(
    streaming_response: StreamingResponse,
    chain: MagicMock,
    send: AsyncMock,
    background: BackgroundTask,
) -> None:
    chain.acall.side_effect = Exception("Something went wrong")

    await streaming_response.stream_response(send)

    assert background.kwargs["outputs"] == "Something went wrong"


@pytest.mark.asyncio
async def test_streaming_json_create_chain_executor(
    chain: MagicMock, inputs: dict[str, str], send
) -> None:
    chain_executor = StreamingResponse._create_chain_executor(
        chain=chain, inputs=inputs, as_json=True
    )

    assert callable(chain_executor)

    chain.acall.assert_not_called()

    await chain_executor(send)

    chain.acall.assert_called_once_with(
        inputs=inputs, callbacks=[get_streaming_json_callback(chain=chain, send=send)]
    )
