# API Reference

This is Lanarky's API reference documentation.

The API reference in split into multiple sections. First, we will cover the
Core API:

- [`Lanarky`](./lanarky.md) - The main application module
- [`StreamingResponse`](./streaming.md) - `Response` class for streaming
- [`WebSocketSession`](./websockets.md) - class for managing websocket sessions

!!! note

    Lanarky also provides a collection of web clients for testing purposes.
    See [Miscellaneous](./misc.md) for more information.

Next, we will cover the Adapter API:

- [OpenAI](./adapters/openai.md): Adapter module for
  [OpenAI Python SDK](https://platform.openai.com/docs/api-reference?lang=python)
- [LangChain](./adapters/langchain.md): Adapter module for
  [LangChain](https://www.langchain.com/)

You can find all other utility functions/classes in the [Miscellaneous](./misc.md) section.
