<div align="center">

<img src="https://raw.githubusercontent.com/ajndkr/lanarky/main/assets/logo-light-mode.png#gh-light-mode-only" alt="lanarky-logo-light-mode" width="500">

<h4>The web framework for building LLM microservices.</h4>

[![Stars](https://img.shields.io/github/stars/ajndkr/lanarky)](https://github.com/ajndkr/lanarky/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ajndkr/lanarky/blob/main/LICENSE)
[![Twitter](https://img.shields.io/twitter/follow/LanarkyAPI?style=social)](https://twitter.com/intent/follow?screen_name=LanarkyAPI)
[![Discord](https://img.shields.io/badge/join-Discord-7289da.svg)](https://discord.gg/6qUfrQAEeE)

[![Python](https://img.shields.io/pypi/pyversions/lanarky.svg)](https://pypi.org/project/lanarky/)
[![Coverage](https://coveralls.io/repos/github/ajndkr/lanarky/badge.svg?branch=main)](https://coveralls.io/github/ajndkr/lanarky?branch=main)
[![Version](https://badge.fury.io/py/lanarky.svg)](https://pypi.org/project/lanarky/)
[![Stats](https://img.shields.io/pypi/dm/lanarky.svg)](https://pypistats.org/packages/lanarky)

</div>

Lanarky is a **python (3.9+)** web framework for developers who want to build microservices using LLMs.
Here are some of its key features:

- **LLM-first**: Unlike other web frameworks, lanarky is built specifically for LLM developers.
  It's unopinionated in terms of how you build your microservices and guarantees zero vendor lock-in
  with any LLM tooling frameworks or cloud providers
- **Fast & Modern**: Built on top of FastAPI, lanarky offers all the FastAPI features you know and love.
  If you are new to FastAPI, visit [fastapi.tiangolo.com](https://fastapi.tiangolo.com) to learn more
- **Streaming**: Streaming is essential for many real-time LLM applications, like chatbots. Lanarky has
  got you covered with built-in streaming support over **HTTP** and **WebSockets**.
- **Open-source**: Lanarky is open-source and free to use. Forever.

To learn more about lanarky and get started, you can find the full documentation on [lanarky.ajndkr.com](https://lanarky.ajndkr.com)

## Installation

The library is available on PyPI and can be installed via `pip`:

```bash
pip install lanarky
```

## Getting Started

Lanarky provides a powerful abstraction layer to allow developers to build
simple LLM microservices in just a few lines of code.

Here's an example to build a simple microservice that uses OpenAI's `ChatCompletion` service:

```python
from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.routing import OpenAIAPIRouter

app = Lanarky()
router = OpenAIAPIRouter()


@router.post("/chat")
def chat(stream: bool = True) -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(stream=stream, system=system)


app.include_router(router)
```

Visit [Getting Started](https://lanarky.ajndkr.com/getting-started) for the full tutorial on building
and testing your first LLM microservice with Lanarky.

## Contributing

[![Code check](https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml/badge.svg)](https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml)
[![Publish](https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml/badge.svg)](https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml)

Contributions are more than welcome! If you have an idea for a new feature or want to help improve lanarky,
please create an issue or submit a pull request on [GitHub](https://github.com/ajndkr/lanarky).

See [CONTRIBUTING.md](https://github.com/ajndkr/lanarky/blob/main/CONTRIBUTING.md) for more information.

## License

The library is released under the [MIT License](https://github.com/ajndkr/lanarky/blob/main/LICENSE).
