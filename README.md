<div align="center">

<img src="https://raw.githubusercontent.com/ajndkr/lanarky/main/assets/logo.png" alt="lanarky-logo" width="250">

<h1> Lanarky </h1>

[![stars](https://img.shields.io/github/stars/ajndkr/lanarky)](https://github.com/ajndkr/lanarky/stargazers)
[![Documentation](https://img.shields.io/badge/documentation-ReadTheDocs-blue.svg)](https://lanarky.readthedocs.io/en/latest/)
[![Code Coverage](https://coveralls.io/repos/github/ajndkr/lanarky/badge.svg?branch=main)](https://coveralls.io/github/ajndkr/lanarky?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ajndkr/lanarky/blob/main/LICENSE)
[![Twitter](https://img.shields.io/twitter/follow/lanarky_io?style=social)](https://twitter.com/intent/follow?screen_name=lanarky_io)

[![PyPI version](https://badge.fury.io/py/lanarky.svg)](https://pypi.org/project/lanarky/)
[![PyPI stats](https://img.shields.io/pypi/dm/lanarky.svg)](https://pypistats.org/packages/lanarky)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/lanarky.svg)](https://pypi.org/project/lanarky/)

</div>

A [FastAPI](https://github.com/tiangolo/fastapi) framework to build production-grade LLM applications.

</div>
<details>
<summary><strong>Table of Contents</strong></summary>

- [🚀 Features](#-features)
- [❓ Why?](#-why)
- [💾 Installation](#-installation)
- [🔥 Build your first LLM app](#-build-your-first-llm-app)
- [📍 Roadmap](#-roadmap)
- [🤩 Stargazers](#-stargazers)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [✨ Want to build LLM applications with us?](#-want-to-build-llm-applications-with-us)

</details>

## 🚀 Features

- 🌐 multi-mode token streaming
- 💬 Gradio plugin for fast prototyping
- 🔗 supports [LangChain](https://github.com/hwchase17/langchain)
- 🗄️ multiple LLM caching strategies

See [Roadmap](#-roadmap) for upcoming features.

## ❓ Why?

Many open-source projects for developing and deploying LLM applications have either opinionated designs,
particularly regarding deployment, or limitations in terms of scalability. This is where Lanarky comes in.
Lanarky is an open-source project that provides Python users with an unopinionated web framework for constructing
and deploying LLM applications. By leveraging FastAPI as its foundation, Lanarky ensures that applications built
with it are production-ready and can be seamlessly deployed on any cloud provider.

## 💾 Installation

The library is available on PyPI and can be installed via `pip`.

```bash
pip install lanarky
```

You can find the full documentation at [https://lanarky.readthedocs.io/en/latest/](https://lanarky.readthedocs.io/en/latest/).

## 🔥 Build your first Langchain app

```python
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI

from lanarky import LangchainRouter

load_dotenv()
app = FastAPI()

langchain_router = LangchainRouter(
    langchain_url="/chat",
    langchain_object=ConversationChain(
        llm=ChatOpenAI(temperature=0), verbose=True
    ),
    streaming_mode=0
  )
app.include_router(langchain_router)
```

See [`examples/`](https://github.com/ajndkr/lanarky/blob/main/examples/README.md)
for list of available demo examples.

Create a `.env` file using `.env.sample` and add your OpenAI API key to it
before running the examples.

![demo](https://raw.githubusercontent.com/ajndkr/lanarky/main/assets/demo.gif)

## 📍 Roadmap

- [x] Add support for [LangChain](https://github.com/hwchase17/langchain)
- [x] Add [Gradio](https://github.com/gradio-app/gradio) UI for fast prototyping
- [x] Add support for in-memory, Redis and [GPTCache](https://github.com/zilliztech/GPTCache) LLM caching
- [ ] Add support for [LlamaIndex](https://github.com/jerryjliu/llama_index)
- [ ] Add support for [Guidance](https://github.com/microsoft/guidance)
- [ ] Add SQL database integration
- [ ] Add support for [Rebuff](https://github.com/woop/rebuff)

## 🤩 Stargazers

Leave a ⭐ if you find this project useful.

[![Star History Chart](https://api.star-history.com/svg?repos=ajndkr/lanarky&type=Date)](https://star-history.com/#ajndkr/lanarky&Date)

## 🤝 Contributing

[![Code check](https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml/badge.svg)](https://github.com/ajndkr/lanarky/actions/workflows/code-check.yaml)
[![Publish](https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml/badge.svg)](https://github.com/ajndkr/lanarky/actions/workflows/publish.yaml)

Contributions are more than welcome! If you have an idea for a new feature or want to help improve lanarky,
please create an issue or submit a pull request on [GitHub](https://github.com/ajndkr/lanarky).

See [CONTRIBUTING.md](https://github.com/ajndkr/lanarky/blob/main/CONTRIBUTING.md) for more information.

### Contributors

[![](https://img.shields.io/github/contributors-anon/ajndkr/lanarky)](https://github.com/ajndkr/lanarky/graphs/contributors)

<a href="https://github.com/ajndkr/lanarky/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ajndkr/lanarky" />
</a>

## ⚖️ License

The library is released under the [MIT License](https://github.com/ajndkr/lanarky/blob/main/LICENSE).

## ✨ Want to build LLM applications with us?

Are you interested in building LLM applications with us? We would love to hear from you! Reach out to us on
Twitter [@lanarky_io](https://twitter.com/lanarky_io).

Let's connect and explore the possibilities of working together to create amazing LLM applications with Lanarky!
