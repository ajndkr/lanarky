---
hide:
  - toc
---

FastAPI offers a powerful [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
system that allows you to inject dependencies into your API endpoints. Lanarky extends this functionality
by offering LangChain as a dependency.

!!! example "Experimental"

    LLM-based dependency injection is an experimental feature. We will add more functionality
    based on community feedback and viable use cases. If you have ideas or suggestions, we
    would love to hear from you. Feel free to open an issue on
    [GitHub](https://github.com/ajndkr/lanarky/issues/new/choose).

Let's take a look at how we can use LangChain as a dependency.

```python
import os

from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)

from lanarky import Lanarky
from lanarky.adapters.langchain.dependencies import Depends

os.environ["OPENAI_API_KEY"] = "add-your-openai-api-key-here"


app = Lanarky()


def chain_factory(temperature: float = 0.0, verbose: bool = False) -> LLMChain:
    return LLMChain(
        llm=ChatOpenAI(temperature=temperature),
        prompt=ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate.from_template("Respond in JSON: {input}")
                ),
            ]
        ),
        verbose=verbose,
    )


@app.post("/")
async def endpoint(outputs: dict = Depends(chain_factory)):
    return outputs["text"]
```

In the above example, we pass `chain_factory` as a dependency to the endpoint. The endpoint
exposes the dependency function arguments as query parameters. This allows us to configure
the dependency at runtime.

To test the above endpoint, let's create a client script:

```python
import click
import httpx


@click.command()
@click.option("--input", required=True)
def main(input: str):
    url = "http://localhost:8000/"

    with httpx.Client() as client:
        response = client.post(url, json={"input": input})
        if response.status_code == 200:
            data = response.json()
            print(f"Received: {data}")
        else:
            print(response.text)


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
  "team": "Los Angeles Dodgers",
  "year": 2020
}
```
