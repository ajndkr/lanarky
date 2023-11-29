import json
from contextlib import contextmanager
from typing import Any, Iterator, Optional

import httpx
from httpx_sse import ServerSentEvent, connect_sse
from websockets.sync.client import connect as websocket_connect

from lanarky.websockets import DataMode


class StreamingClient:
    """Test client for streaming server-sent events."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        client: Optional[httpx.Client] = None,
    ):
        """Constructor method.

        Args:
            base_url: The base URL of the server.
            client: The HTTP client to use.
        """
        self.base_url = base_url
        self.client = client or httpx.Client()

    def stream_response(
        self, method: str, path: str, **kwargs: dict[str, Any]
    ) -> Iterator[ServerSentEvent]:
        """Stream data from the server.

        Args:
            method: The HTTP method to use.
            path: The path to stream from.
            **kwargs: The keyword arguments to pass to the HTTP client.
        """
        url = self.base_url + path
        with connect_sse(self.client, method, url, **kwargs) as event_source:
            for sse in event_source.iter_sse():
                yield sse


class WebSocketClient:
    """Test client for WebSockets.

    Supports 3 data modes: JSON, TEXT, and BYTES.
    """

    def __init__(
        self, uri: str = "ws://localhost:8000/ws", mode: DataMode = DataMode.JSON
    ):
        """Constructor method.

        Args:
            uri: The URI of the websocket.
            mode: The data mode to use.
        """
        self.uri = uri
        self.mode = mode
        self.websocket = None

    @contextmanager
    def connect(self):
        """Connect to a websocket and yield data from it."""
        with websocket_connect(self.uri) as websocket:
            self.websocket = websocket
            yield self
            self.websocket = None

    def send(self, message: Any):
        """Send data to the websocket.

        Args:
            message: The data to send.
        """
        if self.websocket:
            if self.mode == DataMode.JSON:
                message = json.dumps(message)
            elif self.mode == DataMode.TEXT:
                message = str(message)
            elif self.mode == DataMode.BYTES:
                message = message.encode("utf-8")
            self.websocket.send(message)

    def receive(self, mode: DataMode = None):
        """Receive data from the websocket.

        Args:
            mode: The data mode to use.
        """
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
        """Stream data from the websocket.

        Streaming stops until the websocket is closed or
        the `end` event is received.
        """
        if self.websocket:
            while True:
                response = self.receive(mode=DataMode.JSON)
                if response["event"] == "end":
                    break
                yield response
