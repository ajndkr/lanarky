import json
from contextlib import contextmanager
from typing import Any, Generator, Optional

import httpx
from httpx_sse import connect_sse
from websockets.sync.client import connect as websocket_connect

from lanarky.websockets import DataMode


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


class WebSocketClient:
    def __init__(
        self, uri: str = "ws://localhost:8000/ws", mode: DataMode = DataMode.JSON
    ):
        self.uri = uri
        self.mode = mode
        self.websocket = None

    @contextmanager
    def connect(self):
        with websocket_connect(self.uri) as websocket:
            self.websocket = websocket
            yield self
            self.websocket = None

    def send(self, message: Any):
        if self.websocket:
            if self.mode == DataMode.JSON:
                message = json.dumps(message)
            elif self.mode == DataMode.TEXT:
                message = str(message)
            elif self.mode == DataMode.BYTES:
                message = message.encode("utf-8")
            self.websocket.send(message)

    def receive(self, mode: DataMode = None):
        mode = mode or self.mode
        if self.websocket:
            response = self.websocket.recv()
            if mode == DataMode.JSON:
                response = json.loads(response)
            elif mode == DataMode.TEXT:
                response = str(response)
            elif mode == DataMode.BYTES:
                response = response.decode("utf-8")
            return response

    def stream_response(self):
        if self.websocket:
            while True:
                response = self.receive(mode=DataMode.JSON)
                if response["event"] == "end":
                    break
                yield response
