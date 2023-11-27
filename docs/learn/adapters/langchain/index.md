# LangChain Adapter

The **LangChain Adapter** allows Lanarky users to build microservices using the
[LangChain](https://www.langchain.com/) framework.

To enable this adapter, install lanarky with extra dependencies:

<!-- termynal -->

```
$ pip install lanarky[langchain]
```

!!! tip

    LangChain is an LLM tooling framework to construct LLM chains and agents using
    LLM providers such OpenAI, Anthropic, etc. Visit their [Python SDK](https://python.langchain.com/docs/)
    documentation for more information.

Here's an overview of the supported features:

- [Langchain API Router](./router.md): Lanarky router for LangChain
- [Callbacks](./callbacks.md): collection of Lanarky callbacks for LangChain

Additionally, we will cover some advanced topics:

- [Dependency Injection](./dependency.md): use LangChain as a dependency in your microservice
- [FastAPI Backport](./fastapi.md): low-level modules for FastAPI users
