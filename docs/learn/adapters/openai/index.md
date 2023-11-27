# OpenAI Adapter

The **OpenAI Adapter** allows Lanarky users to build microservices using the
[OpenAI Python SDK](https://platform.openai.com/docs/api-reference?lang=python).

To enable this adapter, install lanarky with extra dependencies:

<!-- termynal -->

```
$ pip install lanarky[openai]
```

!!! info

    To use OpenAI, you need to create an openai account and generate an API key.
    Visit [openai.com](https://openai.com) for more information.

    To use the generated API key, you need to set the `OPENAI_API_KEY` environment
    variable.

Here's an overview of the supported features:

- [OpenAI API Router](./router.md): Lanarky router for OpenAI
- [Dependency Injection](./dependency.md): use OpenAI as a dependency in your microservice
- [FastAPI Backport](./fastapi.md): low-level modules for FastAPI users
