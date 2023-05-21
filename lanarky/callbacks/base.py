from abc import abstractmethod
from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field
from starlette.types import Message, Send

from lanarky.schemas import WebsocketResponse


class AsyncLanarkyCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI StreamingResponse."""

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def _construct_message(self, message: str) -> Any:  # pragma: no cover
        """Construct a Message from a string."""
        pass


class AsyncStreamingResponseCallback(AsyncLanarkyCallback):
    """Async Callback handler for FastAPI StreamingResponse."""

    send: Send = Field(...)

    def _construct_message(self, message_str: str) -> Message:
        """Construct a Message from a string."""
        return {"type": "http.response.body", "body": message_str, "more_body": True}


class AsyncWebsocketCallback(AsyncLanarkyCallback):
    """Async Callback handler for FastAPI websocket connection."""

    websocket: WebSocket = Field(...)
    response: WebsocketResponse = Field(...)

    def _construct_message(self, message_str: str) -> dict:
        """Construct a WebsocketResponse from a string."""
        return {**self.response.dict(), **{"message": message_str}}
