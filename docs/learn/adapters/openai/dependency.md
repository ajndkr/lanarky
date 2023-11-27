---
hide:
  - toc
---

FastAPI offers a powerful [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
system that allows you to inject dependencies into your API endpoints. Lanarky extends this functionality
by offering OpenAI as a dependency.

!!! example "Experimental"

    LLM-based dependency injection is an experimental feature. We will add more functionality
    based on community feedback and viable use cases. If you have ideas or suggestions, we
    would love to hear from you. Feel free to open an issue on
    [GitHub](https://github.com/ajndkr/lanarky/issues/new/choose).

Let's take a look at how we can use OpenAI as a dependency.

```python
import os

from lanarky import Lanarky
from lanarky.adapters.openai.dependencies import Depends
from lanarky.adapters.openai.resources import ChatCompletion, ChatCompletionResource

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"

app = Lanarky()


def chat_completion_factory() -> ChatCompletionResource:
    return ChatCompletionResource(
        system="You are a helpful assistant designed to output JSON.",
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
    )


@app.post("/")
async def endpoint(outputs: ChatCompletion = Depends(chat_completion_factory)):
    return outputs.choices[0].message.content
```

In the above example, we pass `chat_completion_factory` as a dependency to the `POST /` endpoint.
Similar to how FasAPI handles dependencies, you can expose additional parameters by defining arguments
in the `chat_completion_factory` function. For example, if you want to expose the `temperature` parameter,
you can do so by adding a `temperature` argument to the `chat_completion_factory` function.

```python
def chat_completion_factory(temperature: float = 0.5) -> ChatCompletionResource:
    return ChatCompletionResource(
        system="You are a helpful assistant designed to output JSON.",
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        temperature=temperature,
    )
```

To test the above endpoint, let's create a client script:

```python
import click
import httpx


@click.command()
@click.option("--input", required=True)
def main(input: str):
    url = "http://localhost:8000/"

    with httpx.Client() as client:
        response = client.post(
            url, json={"messages": [dict(role="user", content=input)]}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Received: {data}")


if __name__ == "__main__":
    main()
```

First, start the server:

```bash
uvicorn app:app
```

Then, run the client script:

<!-- termynal -->

```
$ python client.py --input "Who won the world series in 2020?"
Received: {
  "result": "The Los Angeles Dodgers won the World Series in 2020."
}
```
