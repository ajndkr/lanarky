# ChatGPT-clone

A chatbot application like [ChatGPT](https://chat.openai.com/), built with Lanarky.

This example covers the following Lanarky features:

- OpenAI Adapter
- Streaming tokens via server-sent events

To learn more about Lanarky, check out Lanarky's [full documentation](https://lanarky.ajndkr.com/learn/).

## Setup

Install dependencies:

```
pip install 'lanarky[openai]' gradio
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
