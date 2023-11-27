---
hide:
  - toc
---

Lanarky uses [Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
to implement streaming support over HTTP.

## `StreamingResponse`

The `StreamingResponse` class follows the [`EventSource`](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)
protocol to send events to the client.

### Example

To understand how to use `StreamingResponse`, let's look at an example.

```python
from lanarky import Lanarky
from lanarky.responses import StreamingResponse

app = Lanarky()


@app.get("/")
def index():
    def stream():
        for word in ["Hello", "World!"]:
            yield word

    return StreamingResponse(content=stream())
```

Here, we have a simple endpoint streams the message "Hello World!" to the client.
`StreamingResponse` takes a generator function as its content, iterates over it and
sends each item as an event to the client.

To receive the events, let's build a simple client script.

```python
from lanarky.clients import StreamingClient


def main():
    client = StreamingClient()
    for event in client.stream_response("GET", "/"):
        print(f"{event.event}: {event.data}")


if __name__ == "__main__":
    main()
```

First run the application server.

<!-- termynal -->

```
$ uvicorn app:app
```

Then run the client script.

<!-- termynal -->

```
$ python client.py
message: Hello
message: World!
```

!!! warning

    The `StreamingResponse` classes inside the **Adapters API** behave differently from the
    above example. To learn more, see [Adapters API](./adapters/index.md) documentation.
