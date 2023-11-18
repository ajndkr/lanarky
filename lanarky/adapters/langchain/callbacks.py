from enum import Enum
from typing import Any, Optional, Union

from fastapi.websockets import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.globals import get_llm_cache
from pydantic import BaseModel
from sse_starlette.sse import ServerSentEvent, ensure_bytes
from starlette.types import Message, Send


class LanarkyCallbackHandler(AsyncCallbackHandler):
    """Base callback handler for Lanarky applications."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.llm_cache_used = get_llm_cache() is not None

    @property
    def llm_cache_enabled(self) -> bool:
        """Determine if LLM caching is enabled."""
        return get_llm_cache() is not None

    @property
    def always_verbose(self) -> bool:
        """Verbose mode is always enabled for Lanarky applications."""
        return True


class Events(str, Enum):
    COMPLETION = "completion"
    SOURCE_DOCUMENTS = "source_documents"


class StreamingCallbackHandler(LanarkyCallbackHandler):
    """Callback handler for streaming responses."""

    def __init__(
        self,
        send: Send = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._send = send

    @property
    def send(self) -> Send:
        return self._send

    @send.setter
    def send(self, value: Send) -> None:
        """Setter method for send property."""
        if not callable(value):
            raise ValueError("value must be a Callable")
        self._send = value

    def _construct_message(
        self, data: Union[str, dict[str, Any]], event: Optional[str] = None
    ) -> Message:
        """Constructs message payload"""
        chunk = ServerSentEvent(data=data, event=event)
        return {
            "type": "http.response.body",
            "body": ensure_bytes(chunk, None),
            "more_body": True,
        }


class TokenStreamMode(str, Enum):
    TEXT = "text"
    JSON = "json"


class TokenEventData(BaseModel):
    """Event data payload for tokens."""

    token: str = ""


def get_token_data(token: str, mode: TokenStreamMode) -> Union[str, dict[str, Any]]:
    """Get token data based on mode."""
    if mode == TokenStreamMode.TEXT:
        return token
    else:
        return TokenEventData(token=token).model_dump()


class TokenStreamingCallbackHandler(StreamingCallbackHandler):
    """Callback handler for streaming tokens."""

    def __init__(
        self,
        output_key: str,
        mode: TokenStreamMode = TokenStreamMode.TEXT,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.output_key = output_key

        if mode not in list(TokenStreamMode):
            raise ValueError(f"Invalid stream mode: {mode}")
        self.mode = mode

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if self.llm_cache_used:  # cache missed (or was never enabled) if we are here
            self.llm_cache_used = False

        message = self._construct_message(
            data=get_token_data(token, self.mode), event=Events.COMPLETION
        )
        await self.send(message)

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running.

        Final output is streamed only if LLM cache is enabled.
        """
        if self.llm_cache_used:
            if self.output_key in outputs:
                message = self._construct_message(
                    data=get_token_data(outputs[self.output_key], self.mode),
                    event=Events.COMPLETION,
                )
                await self.send(message)
            else:
                raise KeyError(f"missing outputs key: {self.output_key}")


class SourceDocumentsEventData(BaseModel):
    """Event data payload for source documents."""

    source_documents: list[dict[str, Any]]


class SourceDocumentsStreamingCallbackHandler(StreamingCallbackHandler):
    """Callback handler for streaming source documents."""

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            # NOTE: langchain is using pydantic_v1 for `Document`
            source_documents: list[dict] = [
                document.dict() for document in outputs["source_documents"]
            ]
            message = self._construct_message(
                data=SourceDocumentsEventData(
                    source_documents=source_documents
                ).model_dump(),
                event=Events.SOURCE_DOCUMENTS,
            )
            await self.send(message)


class FinalTokenStreamingCallbackHandler(
    TokenStreamingCallbackHandler, FinalStreamingStdOutCallbackHandler
):
    """Callback handler for streaming final answer tokens.

    Useful for streaming responses from Langchain Agents.
    """

    def __init__(
        self,
        answer_prefix_tokens: Optional[list[str]] = None,
        strip_tokens: bool = True,
        stream_prefix: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        FinalStreamingStdOutCallbackHandler.__init__(
            self,
            answer_prefix_tokens=answer_prefix_tokens,
            strip_tokens=strip_tokens,
            stream_prefix=stream_prefix,
        )

    async def on_llm_start(self, *args, **kwargs) -> None:
        self.answer_reached = False

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # Remember the last n tokens, where n = len(answer_prefix_tokens)
        self.append_to_last_tokens(token)

        # Check if the last n tokens match the answer_prefix_tokens list ...
        if self.check_if_answer_reached():
            self.answer_reached = True
            if self.stream_prefix:
                message = self._construct_message(
                    data=get_token_data(self.last_tokens, self.mode),
                    event=Events.COMPLETION,
                )
                await self.send(message)

        # ... if yes, then print tokens from now on
        if self.answer_reached:
            message = self._construct_message(
                data=get_token_data(token, self.mode), event=Events.COMPLETION
            )
            await self.send(message)


class WebSocketCallbackHandler(LanarkyCallbackHandler):
    """Callback handler for websocket sessions."""

    def __init__(
        self,
        mode: TokenStreamMode = TokenStreamMode.TEXT,
        websocket: WebSocket = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        if mode not in list(TokenStreamMode):
            raise ValueError(f"Invalid stream mode: {mode}")
        self.mode = mode

        self._websocket = websocket

    @property
    def websocket(self) -> Send:
        return self._websocket

    @websocket.setter
    def websocket(self, value: WebSocket) -> None:
        """Setter method for send property."""
        if not isinstance(value, WebSocket):
            raise ValueError("value must be a WebSocket")
        self._websocket = value

    def _construct_message(
        self, data: Union[str, dict[str, Any]], event: Optional[str] = None
    ) -> Message:
        """Constructs message payload"""
        return dict(data=data, event=event)


class TokenWebSocketCallbackHandler(WebSocketCallbackHandler):
    """Callback handler for sending tokens in websocket sessions."""

    def __init__(self, output_key: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.output_key = output_key

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if self.llm_cache_used:  # cache missed (or was never enabled) if we are here
            self.llm_cache_used = False

        message = self._construct_message(
            data=get_token_data(token, self.mode), event=Events.COMPLETION
        )
        await self.websocket.send_json(message)

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running.

        Final output is streamed only if LLM cache is enabled.
        """
        if self.llm_cache_used:
            if self.output_key in outputs:
                message = self._construct_message(
                    data=get_token_data(outputs[self.output_key], self.mode),
                    event=Events.COMPLETION,
                )
                await self.websocket.send_json(message)
            else:
                raise KeyError(f"missing outputs key: {self.output_key}")


class SourceDocumentsWebSocketCallbackHandler(WebSocketCallbackHandler):
    """Callback handler for sending source documents in websocket sessions."""

    async def on_chain_end(self, outputs: dict[str, Any], **kwargs: Any) -> None:
        """Run when chain ends running."""
        if "source_documents" in outputs:
            # NOTE: langchain is using pydantic_v1 for `Document`
            source_documents: list[dict] = [
                document.dict() for document in outputs["source_documents"]
            ]
            message = self._construct_message(
                data=SourceDocumentsEventData(
                    source_documents=source_documents
                ).model_dump(),
                event=Events.SOURCE_DOCUMENTS,
            )
            await self.websocket.send_json(message)


class FinalTokenWebSocketCallbackHandler(
    TokenWebSocketCallbackHandler, FinalStreamingStdOutCallbackHandler
):
    """Callback handler for sending final answer tokens in websocket sessions.

    Useful for streaming responses from Langchain Agents.
    """

    def __init__(
        self,
        answer_prefix_tokens: Optional[list[str]] = None,
        strip_tokens: bool = True,
        stream_prefix: bool = False,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        FinalStreamingStdOutCallbackHandler.__init__(
            self,
            answer_prefix_tokens=answer_prefix_tokens,
            strip_tokens=strip_tokens,
            stream_prefix=stream_prefix,
        )

    async def on_llm_start(self, *args, **kwargs) -> None:
        self.answer_reached = False

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # Remember the last n tokens, where n = len(answer_prefix_tokens)
        self.append_to_last_tokens(token)

        # Check if the last n tokens match the answer_prefix_tokens list ...
        if self.check_if_answer_reached():
            self.answer_reached = True
            if self.stream_prefix:
                message = self._construct_message(
                    data=get_token_data(self.last_tokens, self.mode),
                    event=Events.COMPLETION,
                )
                await self.websocket.send_json(message)

        # ... if yes, then print tokens from now on
        if self.answer_reached:
            message = self._construct_message(
                data=get_token_data(token, self.mode), event=Events.COMPLETION
            )
            await self.websocket.send_json(message)
