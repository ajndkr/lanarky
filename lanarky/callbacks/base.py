import json
from abc import abstractmethod
from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field
from starlette.types import Message, Send

from lanarky.schemas import StreamingJSONResponse, WebsocketResponse


class AsyncLanarkyCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI StreamingResponse."""

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def _construct_message(self, content: Any) -> Any:  # pragma: no cover
        """Construct a Message from a string."""
        pass


class AsyncStreamingResponseCallback(AsyncLanarkyCallback):
    """Async Callback handler for StreamingResponse."""

    send: Send = Field(...)

    def _construct_message(self, content: str) -> Message:
        """Construct a Message from a string."""
        return {
            "type": "http.response.body",
            "body": content.encode("utf-8"),
            "more_body": True,
        }


class AsyncWebsocketCallback(AsyncLanarkyCallback):
    """Async Callback handler for WebsocketConnection."""

    websocket: WebSocket = Field(...)
    response: WebsocketResponse = Field(...)

    def _construct_message(self, content: str) -> dict:
        """Construct a WebsocketResponse from a string."""
        return {**self.response.dict(), **{"message": content.encode("utf-8")}}


class AsyncStreamingJSONResponseCallback(AsyncStreamingResponseCallback):
    """Async Callback handler for StreamingJSONResponse."""

    send: Send = Field(...)

    def _construct_message(self, content: StreamingJSONResponse) -> Message:
        """Construct a Message from a dictionary."""
        return {
            "type": "http.response.body",
            "body": json.dumps(
                content.dict(),
                ensure_ascii=False,
                allow_nan=False,
                indent=None,
                separators=(",", ":"),
            ).encode("utf-8"),
            "more_body": True,
        }
