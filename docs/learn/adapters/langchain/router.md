# LangChain API Router

The `LangChainAPIRouter` class is an abstraction layer which provides a quick and easy
way to build microservices using LangChain.

Let's understand how to use `LangChainAPIRouter` to build streaming and websocket
endpoints.

## Streaming

```python
import os

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

from lanarky import Lanarky
from lanarky.adapters.langchain.routing import LangchainAPIRouter

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()
router = LangchainAPIRouter()


@router.post("/chat")
def chat(
    temperature: float = 0.0, verbose: bool = False, streaming: bool = True
) -> ConversationChain:
    return ConversationChain(
        llm=ChatOpenAI(temperature=temperature, streaming=streaming),
        verbose=verbose,
    )


app.include_router(router)
```

In this example, we use `chat` as a `ConversationChain` factory function and send it
to the router to build a streaming endpoint. The additional parameters such as
`temperature`, `verbose`, and `streaming` are exposed as query parameters.

To receive the events, we will use the following client script:

```python
import json

import click

from lanarky.clients import StreamingClient


@click.command()
@click.option("--input", required=True)
@click.option("--stream", is_flag=True)
def main(input: str, stream: bool):
    client = StreamingClient()
    for event in client.stream_response(
        "POST",
        "/chat",
        params={"streaming": str(stream).lower()},
        json={"input": input},
    ):
        print(f"{event.event}: {json.loads(event.data)['token']}", end="", flush=True)


if __name__ == "__main__":
    main()
```

First run the application server:

<!-- termynal -->

```
$ uvicorn app:app
```

Then run the client script:

<!-- termynal -->

```
$ python client.py --input "hi"
completion: Hello! How can I assist you today?
```

## Websocket

```python
import os

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

from lanarky import Lanarky
from lanarky.adapters.langchain.routing import LangchainAPIRouter

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()
router = LangchainAPIRouter()


@router.websocket("/ws")
def chat() -> ConversationChain:
    return ConversationChain(llm=ChatOpenAI(streaming=True), verbose=True)


app.include_router(router)
```

Similar to the streaming example, we use `chat` as a `ConversationChain` factory
function and send it to the router to build a websocket endpoint.

To communicate with the server, we will use the following client script:

```python
import json
from lanarky.clients import WebSocketClient


def main():
    client = WebSocketClient()
    with client.connect() as session:
        while True:
            user_input = input("\nEnter a message: ")
            session.send(dict(input=user_input))
            print("Received: ", end="")
            for chunk in session.stream_response():
                print(json.loads(chunk["data"])["token"], end="", flush=True)


if __name__ == "__main__":
    main()
```

First run the application server:

<!-- termynal -->

```
$ uvicorn app:app
```

Then run the client script:

<!-- termynal -->

```
$ python client.py
Enter a message: hi
Received: Hello! How can I assist you today?
Enter a message: i am lanarky
Received: Hello Lanarky! It's nice to meet you. How can I assist
you today?
Enter a message: who am i?
Received: You are Lanarky, as you mentioned earlier. Is there anything
specific you would like to know about yourself?
```

!!! note "Note from Author"

    If you want to build more complex logic, I recommend using the low-level modules
    to define the endpoint from scratch: [Learn more](./fastapi.md)
