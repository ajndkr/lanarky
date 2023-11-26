[WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) are useful for
LLM applications which require a bi-directional connection between the client and server.
For example, a chat application would require a WebSocket connection to allow the server to
send messages to the client.

Lanarky builds on top of FastAPI to support LLM applications over WebSockets.
