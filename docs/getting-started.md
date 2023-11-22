---
hide:
  - navigation
---

This is a quick tutorial on getting started with Lanarky.

We will use LangChain as the LLM tooling framework and OpenAI as the LLM provider to
build our first LLM microservice.

## Install Dependencies

<!-- termynal -->

```
$ pip install lanarky[langchain,openai]
```

## Example

We will use the `ConversationChain` from LangChain library to build our first LLM microservice.

!!! info

    You need to set the `OPENAI_API_KEY` environment variable to use OpenAI.
    Visit [openai.com](https://openai.com) to get your API key.

```python
import os
from fastapi import FastAPI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from lanarky.adapters.langchain.routing import LangchainAPIRouter

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"

app = FastAPI()
langchain_router = LangchainAPIRouter()

@langchain_router.post("/chat")
def chat(streaming: bool = True) -> ConversationChain:
    return ConversationChain(llm=ChatOpenAI(streaming=streaming))

app.include_router(langchain_router)
```

Run the application:

<!-- termynal -->

```
$ pip install uvicorn
$ uvicorn app:app --reload
```

View the Swagger docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Testing

<!-- termynal -->

```
$ pip install httpx-sse
```

Create `client.py` script:

```python
import click
import httpx
from httpx_sse import connect_sse


@click.command()
@click.option("--input", required=True)
@click.option("--streaming", is_flag=True)
def main(input: str, streaming: bool):
    url = f"http://localhost:8000/chat?streaming={str(streaming).lower()}"
    with httpx.Client() as client:
        with connect_sse(
            client,
            "POST",
            url,
            json={"input": input},
        ) as event_source:
            for sse in event_source.iter_sse():
                print(sse.event, sse.data)


if __name__ == "__main__":
    main()
```

Stream output:

<!-- termynal -->

```
$ python client.py --input hi --streaming
```

Recieve all output at once:

<!-- termynal -->

```
$ python client.py --input hi
```
