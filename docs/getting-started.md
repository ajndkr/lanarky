---
hide:
  - navigation
---

Let's build our first LLM microservice with Lanarky!

## Install Dependencies

We need to first install some extra dependencies as we will use OpenAI as the LLM
provider.

<!-- termynal -->

```
$ pip install lanarky[openai]
```

## Application

!!! info

    You need to set the `OPENAI_API_KEY` environment variable to use OpenAI.
    Visit [openai.com](https://openai.com) to get your API key.

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

Run application:

<!-- termynal -->

```
$ pip install uvicorn
$ uvicorn app:app --reload
```

!!! info

    Swagger docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Client

Now that the application script is running, we will setup a client script for testing.

Create `client.py`:

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

Since we have exposed only `stream` as the query parameter, we can test 2 scenarios:

1. Recieve output as it is generated:

<!-- termynal -->

```
$ python client.py --input "hi" --stream
$ completion:
$ completion: Well
$ completion: ,
$ completion:  hello
$ completion:  there
$ completion: !
$ completion:  How
$ completion:  can
$ completion:  I
$ completion:  sass
$ completion: ...
$ completion:  I
$ completion:  mean
$ completion:  assist
$ completion:  you
$ completion:  today
$ completion: ?
```

2.  Recieve all output at once:

<!-- termynal -->

```
$ python client.py --input "hi"
$ completion: Oh, hello there! What can I sass...I mean assist you with today?
```
