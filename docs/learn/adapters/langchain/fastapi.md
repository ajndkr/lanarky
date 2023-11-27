Lanarky is built on top of FastAPI and offers backwards compatibility with all FastAPI features.
Nonetheless, if your project uses FastAPI and Lanarky is not a drop-in replacement, you can still
the low-level Lanarky modules to build your microservice.

We will use the examples from the [LangChain API Router](./router.md) guide to demonstrate how to
use the low-level modules as well as understand how the router works under the hood.

## Streaming

LangChain adapter extends the `StreamingResponse` class to support streaming for LangChain microservices.

!!! note

    Before you start, make sure you have read the [Streaming](../../streaming.md) and
    [LangChain API Router](./router.md) guides.

```python
import os

from fastapi import Depends
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from lanarky import Lanarky
from lanarky.adapters.langchain.callbacks import TokenStreamingCallbackHandler
from lanarky.adapters.langchain.responses import StreamingResponse

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()


class ChatInput(BaseModel):
    input: str


def chain_factory(
    temperature: float = 0.0, verbose: bool = False, streaming: bool = True
) -> ConversationChain:
    return ConversationChain(
        llm=ChatOpenAI(temperature=temperature, streaming=streaming),
        verbose=verbose,
    )


@app.post("/chat")
async def chat(
    request: ChatInput,
    chain: ConversationChain = Depends(chain_factory)
):
    return StreamingResponse(
        chain=chain,
        config={
            "inputs": request.model_dump(),
            "callbacks": [
                TokenStreamingCallbackHandler(output_key=chain.output_key),
            ],
        },
    )
```

The `/chat` endpoint is similar to the one we created using `LangChainAPIRouter` in the
[LangChain API Router](./router.md) guide. Besides the `StreamingResponse` class, we also use
the `TokenStreamingCallbackHandler` callback handler to stream the intermediate tokens back to
the client. Check out [Callbacks](../../callbacks.md) to learn more about the lanarky callback
handlers.

!!! tip

    You can use the same client script from the [LangChain API Router](./router.md) guide to test
    the above example.

## Websockets

In addition to streaming, LangChain adapter also supports websockets. Let's take a look at how we can
build an LangChain microservice using websockets.

```python

import os

from fastapi import Depends
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from lanarky import Lanarky
from lanarky.adapters.langchain.callbacks import TokenWebSocketCallbackHandler
from lanarky.events import Events
from lanarky.websockets import WebSocket, WebsocketSession

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()


class ChatInput(BaseModel):
    input: str


def chain_factory() -> ConversationChain:
    return ConversationChain(llm=ChatOpenAI(streaming=True))


@app.websocket("/ws")
async def ws(
    websocket: WebSocket,
    chain: ConversationChain = Depends(chain_factory)
):
    async with WebsocketSession().connect(websocket) as session:
        async for data in session:
            await chain.acall(
                inputs=ChatInput(**data).model_dump(),
                callbacks=[
                    TokenWebSocketCallbackHandler(
                        websocket=websocket, output_key=chain.output_key
                    )
                ],
            )
            await websocket.send_json(dict(data="", event=Events.END))
```

In this example, we use the `WebsocketSession` context manager to connect to the websocket
and communicate with the client. We pass the client data to the `ConversationChain` and stream
the response back to the client.

!!! tip

    Similar to the streaming example, you can use the same client script from the
    [LangChain API Router](./router.md) guide to test the websocket example.
