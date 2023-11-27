# OpenAI API Router

The `OpenAIAPIRouter` class is an abstraction layer which provides a quick and easy
way to build microservices using supported OpenAI models.

!!! warning

    OpenAI SDK support is currently limited to chat models only (i.e.
    GPT-3.5-Turbo, GPT-4 and GPT-4-Turbo). Other models/services will be
    added in the future.

Let's understand how to use `OpenAIAPIRouter` to build streaming and websocket
endpoints.

## Streaming

!!! note

    We are using the example from the [Getting Started](../../../getting-started.md) guide.

```python
import os

from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.routing import OpenAIAPIRouter

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()
router = OpenAIAPIRouter()


@router.post("/chat")
def chat(stream: bool = True) -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(stream=stream, system=system)


app.include_router(router)
```

In this example, `ChatCompletionResource` is a wrapper class to use the OpenAI
Python SDK. `chat` acts as a factory function where we define the parameters of
`ChatCompletionResource` and send it to the router to build the endpoint for us.
The factory function arguments can be used to define query or header parameters
which are exposed to the client.

To receive the events, we will use the following client script:

```python
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
        params={"stream": str(stream).lower()},
        json={"messages": [dict(role="user", content=input)]},
    ):
        print(f"{event.event}: {event.data}")


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
completion: Oh, hello there! What can I sass...I mean assist
you with today?
```

## Websocket

```python
import os

from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.routing import OpenAIAPIRouter

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()
router = OpenAIAPIRouter()


@router.websocket("/ws")
def chat() -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(stream=True, system=system)


app.include_router(router)
```

Similar to the streaming example, we use `chat` as a `ChatCompletionResource`
factory function and send it to the router to build a websocket endpoint.

To communicate with the server, we will use the following client script:

```python
from lanarky.clients import WebSocketClient


def main():
    client = WebSocketClient()
    with client.connect() as session:
        messages = []
        while True:
            user_input = input("\nEnter a message: ")
            messages.append(dict(role="user", content=user_input))
            session.send(dict(messages=messages))
            print("Received: ", end="")
            assistant_message = dict(role="assistant", content="")
            for chunk in session.stream_response():
                print(chunk["data"], end="", flush=True)
                assistant_message["content"] += chunk["data"]
            messages.append(assistant_message)


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
Received: Well, hello there! How can I assist you today?
Enter a message: i am lanarky
Received: Oh, aren't you just full of mischief, Lanarky?
What trouble can I help you stir up today?
Enter a message: who am i?
Received: Well, that's a question only you can answer, Lanarky.
But if I had to guess, based on your sassy spirit, I would say you're
someone who loves to dance to the beat of your own drum and has a
mischievous sense of humor. Am I close?
```

!!! note "Note from Author"

    If you want to build more complex logic, I recommend using the low-level modules
    to define the endpoint from scratch: [Learn more](./fastapi.md)
