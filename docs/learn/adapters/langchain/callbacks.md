Lanarky offers a collection of callback handlers for LangChain. These callback
handlers are useful in executing intermediate callback events related to your LangChain
microservice.

Lanarky offers callback handlers for both streaming and WebSockets. We will take a look at
both of them in this guide.

!!! note

    All callback handlers can be imported from the `lanarky.adapters.langchain.callbacks`
    module.

## Tokens

- `TokenStreamingCallbackHandler`: handles streaming of the intermediate tokens over HTTP
- `TokenWebSocketCallbackHandler`: handles streaming of the intermediate tokens over WebSockets

Both callback handlers offer token streaming in two modes: `text` and `json`. In `text` mode,
the callback handlers will use raw token string as event data. In `json` mode, the callback
handlers will use a JSON object containing the token string as event data.

These callback handlers are useful for all chains where the `llm` component supports streaming.

## Source Documents

- `SourceDocumentStreamingCallbackHandler`: handles streaming of the source documents
  over HTTP
- `SourceDocumentWebSocketCallbackHandler`: handles streaming of the source documents
  over WebSockets

The source documents are sent at the end of a chain execution as a `source_documents` event.

These callback handlers are useful for retrieval-based chains like `RetrievalQA`.

## Agents

- `FinalTokenStreamingCallbackHandler`: handles streaming of the final answer tokens over HTTP
- `FinalTokenWebSocketCallbackHandler`: handles streaming of the final answer tokens over WebSockets

Both callback handlers are extension of the token streaming callback handlers where the tokens are
streamed only when the LLM agent has reached the final step of its execution.

These callback handlers are useful for all agent types like `ZeroShotAgent`.

!!! note

    The callback handlers also inherit some functionality of the `FinalStreamingStdOutCallbackHandler`
    callback handler. Check out [LangChain Docs](https://api.python.langchain.com/en/latest/callbacks/langchain.callbacks.streaming_stdout_final_only.FinalStreamingStdOutCallbackHandler.html) to know more.
