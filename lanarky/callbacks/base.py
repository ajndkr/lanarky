import json
from abc import abstractmethod
from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.globals import get_llm_cache
from starlette.types import Message, Send

from lanarky.schemas import StreamingJSONResponse, WebsocketResponse


class AsyncLanarkyCallback(AsyncCallbackHandler):
    """Async Callback handler for FastAPI StreamingResponse."""

    def __init__(self, output_key: str = "answer", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.output_key = output_key
        self.llm_cache_used = get_llm_cache() is not None

    @property
    def llm_cache_enabled(self) -> bool:
        """Determine if LLM caching is enabled."""
        return get_llm_cache() is not None

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def _construct_message(self, content: Any) -> Any:  # pragma: no cover
        """Constructs a Message from a string."""
        pass


class AsyncStreamingResponseCallback(AsyncLanarkyCallback):
    """Async Callback handler for StreamingResponse."""

    def __init__(self, send: Send, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.send = send

    def _construct_message(self, content: str) -> Message:
        """Constructs a Message from a string."""
        return {
            "type": "http.response.body",
            "body": content.encode("utf-8"),
            "more_body": True,
        }


class AsyncWebsocketCallback(AsyncLanarkyCallback):
    """Async Callback handler for WebsocketConnection."""

    def __init__(
        self, websocket: WebSocket, response: WebsocketResponse, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)

        self.websocket = websocket
        self.response = response

    def _construct_message(self, content: str) -> dict:
        """Constructs a WebsocketResponse from a string."""
        return {**self.response.model_dump(), **{"message": content}}


class AsyncStreamingJSONResponseCallback(AsyncStreamingResponseCallback):
    """Async Callback handler for StreamingJSONResponse."""

    def _construct_message(self, content: StreamingJSONResponse) -> Message:
        """Constructs a Message from a dictionary."""
        return {
            "type": "http.response.body",
            "body": json.dumps(
                content.model_dump(),
                ensure_ascii=False,
                allow_nan=False,
                indent=None,
                separators=(",", ":"),
            ).encode("utf-8"),
            "more_body": True,
        }
