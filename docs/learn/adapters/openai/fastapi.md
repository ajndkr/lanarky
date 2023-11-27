Lanarky is built on top of FastAPI and offers backwards compatibility with all FastAPI features.
Nonetheless, if your project uses FastAPI and Lanarky is not a drop-in replacement, you can still
the low-level Lanarky modules to build your microservice.

We will use the examples from the [OpenAI API Router](./router.md) guide to demonstrate how to
use the low-level modules as well as understand how the router works under the hood.

## Streaming

OpenAI adapter extends the `StreamingResponse` class to support streaming for OpenAI microservices.

!!! note

    Before you start, make sure you have read the [Streaming](../../streaming.md) and
    [OpenAI API Router](./router.md) guides.

```python
import os

from fastapi import Depends
from pydantic import BaseModel

from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource, Message
from lanarky.adapters.openai.responses import StreamingResponse

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"

app = Lanarky()


class ChatInput(BaseModel):
    messages: list[Message]


def chat_completion_factory(stream: bool = True) -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(system=system, stream=stream)


@app.post("/chat")
async def chat(
    request: ChatInput,
    resource: ChatCompletionResource = Depends(chat_completion_factory),
):
    return StreamingResponse(resource=resource, **request.model_dump())
```

The `/chat` endpoint is similar to the one we created using `OpenAIAPIRouter` in the
[OpenAI API Router](./router.md) guide.

!!! tip

    You can use the same client script from the [OpenAI API Router](./router.md) guide to test
    the above example.

## Websockets

In addition to streaming, OpenAI adapter also supports websockets. Let's take a look at how we can
build an OpenAI microservice using websockets.

```python
import os

from fastapi import Depends
from pydantic import BaseModel

from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource, Message
from lanarky.events import Events
from lanarky.websockets import WebSocket, WebsocketSession

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"

app = Lanarky()


class ChatInput(BaseModel):
    messages: list[Message]


def chat_completion_factory(stream: bool = True) -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(system=system, stream=stream)


@app.websocket("/ws")
async def chat(
    websocket: WebSocket,
    resource: ChatCompletionResource = Depends(chat_completion_factory),
):
    async with WebsocketSession().connect(websocket) as session:
        async for data in session:
            async for chunk in resource.stream_response(
                **ChatInput(**data).model_dump()
            ):
                await websocket.send_json(
                    dict(data=chunk, event=Events.COMPLETION)
                )
            await websocket.send_json(dict(data="", event=Events.END))
```

In this example, we use the `WebsocketSession` context manager to connect to the websocket
and communicate with the client. We pass the client data to the OpenAI resource and stream
the response back to the client.

!!! tip

    Similar to the streaming example, you can use the same client script from the
    [OpenAI API Router](./router.md) guide to test the websocket example.
