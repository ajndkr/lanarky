---
hide:
  - toc
---

[WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) are useful for
LLM microservices which require a bi-directional connection between the client and server.
For example, a chat application would require a WebSocket to hold a persistent connection
between the client and server during an active user session.

Lanarky builds on top of FastAPI to support LLM microservices over WebSockets.

## `WebsocketSession`

The `WebsocketSession` class establishes a WebSocket session inside an endpoint logic to define
the interaction between the client and server. This is particularly useful for building chatbot
applications.

### Example

To understand how to use `WebsocketSession`, let's look at an example.

```python
from lanarky import Lanarky
from lanarky.websockets import WebSocket, WebsocketSession

app = Lanarky()


@app.websocket("/ws")
async def endpoint(websocket: WebSocket):
    async with WebsocketSession().connect(websocket) as session:
        async for message in session:
            await websocket.send_json({"data": message["data"].capitalize()})
```

Here, we have a simple websocket endpoint which capitalizes the message sent by the client.
We use the `WebsocketSession` class to establish a session with the client. The session
allows us to send and receive messages from the client.

To receive the events, let's build a simple client script.

```python
from lanarky.clients import WebSocketClient


def main():
    client = WebSocketClient(uri="ws://localhost:8001/ws")
    with client.connect() as session:
        while True:
            user_input = input("Enter a message: ")
            session.send(dict(data=user_input))
            response = session.receive()
            print(f"Received: {response}")


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
Enter a message: hi
Received: {'data': 'Hi'}
Enter a message: hola
Received: {'data': 'Hola'}
```
