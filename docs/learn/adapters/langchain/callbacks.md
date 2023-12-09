Lanarky offers a collection of callback handlers for LangChain. These callback
handlers are useful in executing intermediate callback events related to your LangChain
microservice.

Lanarky offers callback handlers for both streaming and WebSockets. We will take a look at
both of them in this guide.

!!! note

    All callback handlers can be imported from the `lanarky.adapters.langchain.callbacks`
    module.

## Supported Callbacks

Lanarky offers callback handlers for the following events:

### Tokens

- `TokenStreamingCallbackHandler`: handles streaming of the intermediate tokens over HTTP
- `TokenWebSocketCallbackHandler`: handles streaming of the intermediate tokens over WebSockets

Both callback handlers offer token streaming in two modes: `text` and `json`. In `text` mode,
the callback handlers will use raw token string as event data. In `json` mode, the callback
handlers will use a JSON object containing the token string as event data.

These callback handlers are useful for all chains where the `llm` component supports streaming.

### Source Documents

- `SourceDocumentStreamingCallbackHandler`: handles streaming of the source documents
  over HTTP
- `SourceDocumentWebSocketCallbackHandler`: handles streaming of the source documents
  over WebSockets

The source documents are sent at the end of a chain execution as a `source_documents` event.

These callback handlers are useful for retrieval-based chains like `RetrievalQA`.

### Agents

- `FinalTokenStreamingCallbackHandler`: handles streaming of the final answer tokens over HTTP
- `FinalTokenWebSocketCallbackHandler`: handles streaming of the final answer tokens over WebSockets

Both callback handlers are extension of the token streaming callback handlers where the tokens are
streamed only when the LLM agent has reached the final step of its execution.

These callback handlers are useful for all agent types like `ZeroShotAgent`.

!!! note

    The callback handlers also inherit some functionality of the `FinalStreamingStdOutCallbackHandler`
    callback handler. Check out [LangChain Docs](https://api.python.langchain.com/en/latest/callbacks/langchain.callbacks.streaming_stdout_final_only.FinalStreamingStdOutCallbackHandler.html) to know more.

## Create custom lanarky callback handlers

You can create your own lanarky callback handler by inheriting from:

- `StreamingCallbackHandler`: useful for building microservices using server-sent events
- `WebSocketCallbackHandler`: useful for building microservices using WebSockets

For example, let's say you want to create a callback handler for streaming a message at the start of chain:

```python
from lanarky.adapters.langchain.callbacks import StreamingCallbackHandler

class ChainStartStreamingCallbackHandler(StreamingCallbackHandler):
    async def on_chain_start(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        """Run when chain starts running."""
        message = self._construct_message(
            data="Chain started", event="start"
        )
        await self.send(message)
```

When the above callback handler is passed to the input list of callbacks, it will stream the following event:

```
event: start
data: Chain started
```

!!! note

    You can learn more about the specific callback events in the
    [LangChain Docs](https://python.langchain.com/docs/modules/callbacks/)
