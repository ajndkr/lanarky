# fastapi-async-langchain

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ajndkr/fastapi-async-langchain/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/fastapi-async-langchain.svg)](https://pypi.org/project/fastapi-async-langchain/)

Ship production-ready [LangChain](https://github.com/hwchase17/langchain) projects with
[FastAPI](https://github.com/tiangolo/fastapi).

## 🚀 Features

- supports token streaming over HTTP and Websocket
- supports multiple langchain `Chain` types
- simple gradio chatbot UI for fast prototyping
- follows FastAPI responses naming convention

## ❓ Why?

There are great low-code/no-code solutions in the open source to deploy your Langchain projects. However,
most of them are opinionated in terms of cloud or deployment code. This project aims to provide FastAPI users
with a cloud-agnostic and deployment-agnostic solution which can be easily integrated into existing
backend infrastructures.

## 💾 Installation

The library is available on PyPI and can be installed via `pip`.

```bash
pip install fastapi-async-langchain
```

## 🔥 Deploy in under 20 lines of code

```python
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel
from fastapi_async_langchain.responses import StreamingResponse

load_dotenv()
app = FastAPI()

class Request(BaseModel):
    query: str

@app.post("/chat")
async def chat(request: Request) -> StreamingResponse:
    chain = ConversationChain(llm=ChatOpenAI(temperature=0, streaming=True), verbose=True)
    return StreamingResponse.from_chain(chain, request.query, media_type="text/event-stream")
```

See [`examples/`](https://github.com/ajndkr/fastapi-async-langchain/blob/main/examples/README.md) for list of available demo examples.

Create a `.env` file using `.env.sample` and add your OpenAI API key to it
before running the examples.

![demo](https://raw.githubusercontent.com/ajndkr/fastapi-async-langchain/main/assets/demo.gif)

## 🤝 Contributing

[![Code check](https://github.com/ajndkr/fastapi-async-langchain/actions/workflows/code-check.yaml/badge.svg)](https://github.com/ajndkr/fastapi-async-langchain/actions/workflows/code-check.yaml)
[![Publish](https://github.com/ajndkr/fastapi-async-langchain/actions/workflows/publish.yaml/badge.svg)](https://github.com/ajndkr/fastapi-async-langchain/actions/workflows/publish.yaml)

Contributions are more than welcome! If you have an idea for a new feature or want to help improve fastapi-async-langchain, please create an issue or submit a pull request
on [GitHub](https://github.com/ajndkr/fastapi-async-langchain).

See [CONTRIBUTING.md](./CONTRIBUTING.md) for more information.

## ⚖️ License

The library is released under the [MIT License](https://github.com/ajndkr/fastapi-async-langchain/blob/main/LICENSE).
