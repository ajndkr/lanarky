from typing import Any, Callable, Iterator, Union

from fastapi.responses import StreamingResponse
from starlette.types import Send


class NullIterator(Iterator[Union[str, bytes]]):
    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class LangchainStreamingResponse(StreamingResponse):
    """StreamingResponse for langchain LLM chains.

    Credit: https://gist.github.com/ninely/88485b2e265d852d3feb8bd115065b1a
    """

    def __init__(
        self,
        llm_chain_wrapper_fn: Callable,
        **kwargs: Any,
    ) -> None:
        super().__init__(content=NullIterator(), **kwargs)

        self.llm_chain_wrapper_fn = llm_chain_wrapper_fn

    async def stream_response(self, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        async def send_chunk(chunk: Union[str, bytes]):
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)
            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        try:
            await self.llm_chain_wrapper_fn(send_chunk)
        except Exception as e:
            await send(
                {
                    "type": "http.response.body",
                    "body": str(e).encode(self.charset),
                    "more_body": False,
                }
            )

        await send({"type": "http.response.body", "body": b"", "more_body": False})
