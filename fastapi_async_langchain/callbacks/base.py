from abc import abstractproperty

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from pydantic import BaseModel, Field
from starlette.types import Send

from ..schemas import WebsocketResponse


class AsyncStreamingResponseCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI StreamingResponse."""

    send: Send = Field(...)

    @abstractproperty
    def chain_type(self) -> str:
        """The chain type."""
        pass

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True


class AsyncWebsocketCallback(AsyncCallbackHandler, BaseModel):
    """Async Callback handler for FastAPI websocket connection."""

    websocket: WebSocket = Field(...)
    response: WebsocketResponse = Field(...)

    class Config:
        arbitrary_types_allowed = True

    @abstractproperty
    def chain_type(self) -> str:
        """The chain type."""
        pass

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True
