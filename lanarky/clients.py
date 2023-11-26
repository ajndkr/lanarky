from typing import Generator, Optional

import httpx
from httpx_sse import connect_sse


class StreamingClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        client: Optional[httpx.Client] = None,
    ):
        self.base_url = base_url
        self.client = client or httpx.Client()

    def stream_response(self, method: str, path: str, **kwargs) -> Generator:
        url = self.base_url + path
        with connect_sse(self.client, method, url, **kwargs) as event_source:
            for sse in event_source.iter_sse():
                yield sse
