# PaulGPT

A chatbot application to answer questions about Paul Graham essay, "[What I worked on](http://www.paulgraham.com/worked.html)",
built with Lanarky.

This example covers the following Lanarky features:

- LangChain Adapter
- Streaming source documents via server-sent events and websockets

To learn more about Lanarky, check out Lanarky's [full documentation](https://lanarky.ajndkr.com/learn/).

## Setup

Install dependencies:

```
pip install 'lanarky[openai]' gradio faiss-cpu
```

## Run

First we set the OpenAI API key:

```sh
export OPENAI_API_KEY=<your-key>
```

Then we run the server:

```sh
python app.py
```

Once the server is running, open http://localhost:8000/ in your browser.
