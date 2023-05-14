from typing import Any

import requests
from fastapi import FastAPI

from .settings import get_settings


def send_query(api_url: str, query: str, chat: list[Any], history: list[Any]):
    """Adapted code from: https://huggingface.co/spaces/ysharma/Gradio-demo-streaming"""
    history = history or []
    history.append(query)

    payload = {"query": query}
    headers = {
        "accept": "text/event-stream",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }

    try:
        response = requests.post(
            api_url, headers=headers, json=payload, timeout=60, stream=True
        )
        response.raise_for_status()  # Raise stored HTTPError, if one occurred

    except requests.exceptions.HTTPError as httpErr:
        print(f"HTTP error occurred: {httpErr}")
        return
    except requests.exceptions.ConnectionError as connErr:
        print(f"Error connecting: {connErr}")
        return
    except requests.exceptions.Timeout as timeOutErr:
        print(f"Timeout error: {timeOutErr}")
        return
    except requests.exceptions.RequestException as reqErr:
        print(f"Something went wrong with the request: {reqErr}")
        return

    token_counter = 0
    partial_words = ""
    for chunk in response.iter_content(chunk_size=1024):  # Smaller chunk size
        if chunk:
            partial_words = partial_words + chunk.decode()
            if token_counter == 0:
                history.append(" " + partial_words)
            else:
                history[-1] = partial_words
            chat = [(history[i], history[i + 1]) for i in range(0, len(history) - 1, 2)]
            token_counter += 1
            yield chat, history


def clear_chat():
    return [], []


def mount_gradio_app(
    app: FastAPI,
    path: str = get_settings().gradio_path,
    chat_endpoint: str = get_settings().api_endpoint,
    title: str = get_settings().title,
):
    """Mounts a Gradio app on a FastAPI app."""

    try:
        import gradio as gr
    except ImportError:
        raise ImportError(
            "Please install gradio to use this feature: pip install gradio"
        )

    blocks = gr.Blocks(title=title)

    with blocks:
        gr.Markdown(f"<h3><center>{title}</center></h3>")

        with gr.Row():
            query = gr.Textbox(
                label="Enter your question",
                lines=1,
            )
            submit = gr.Button(value="Ask", variant="secondary").style(full_width=False)
            clear = gr.Button(value="Clear", variant="secondary").style(
                full_width=False
            )

        api_url = gr.State(get_settings().api_url + chat_endpoint)
        chatbot = gr.Chatbot()
        history = gr.State()

        submit.click(
            send_query,
            inputs=[api_url, query, chatbot, history],
            outputs=[chatbot, history],
        )
        query.submit(
            send_query,
            inputs=[api_url, query, chatbot, history],
            outputs=[chatbot, history],
        )
        clear.click(
            clear_chat,
            outputs=[chatbot, history],
        )

    return gr.mount_gradio_app(app=app, blocks=blocks.queue(), path=path)
