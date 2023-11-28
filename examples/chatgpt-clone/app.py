import gradio as gr

from lanarky import Lanarky
from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.routing import OpenAIAPIRouter
from lanarky.clients import StreamingClient

app = Lanarky()
router = OpenAIAPIRouter()


@router.post("/chat")
def chat() -> ChatCompletionResource:
    system = "You are a sassy assistant"
    return ChatCompletionResource(system=system, stream=True)


app.include_router(router)


def mount_playground(app: Lanarky) -> Lanarky:
    blocks = gr.Blocks(
        title="ChatGPT-clone",
        theme=gr.themes.Default(
            primary_hue=gr.themes.colors.teal, secondary_hue=gr.themes.colors.teal
        ),
        css="footer {visibility: hidden}",
    )

    with blocks:
        blocks.load(
            None,
            None,
            js="""
            () => {
            document.body.className = "white";
        }""",
        )
        gr.HTML(
            """<div align="center"><img src="https://lanarky.ajndkr.com/assets/logo-light-mode.png" width="350"></div>"""
        )
        chatbot = gr.Chatbot(height=500, show_label=False)
        with gr.Row():
            user_input = gr.Textbox(
                show_label=False, placeholder="Type a message...", scale=5
            )
            clear_btn = gr.Button("Clear")

        def chat(history):
            messages = []
            for human, assistant in history:
                if human:
                    messages.append({"role": "user", "content": human})
                if assistant:
                    messages.append({"role": "assistant", "content": assistant})

            history[-1][1] = ""
            for event in StreamingClient().stream_response(
                "POST", "/chat", json={"messages": messages}
            ):
                history[-1][1] += event.data
                yield history

        user_input.submit(
            lambda user_input, chatbot: ("", chatbot + [[user_input, None]]),
            [user_input, chatbot],
            [user_input, chatbot],
            queue=False,
        ).then(chat, chatbot, chatbot)
        clear_btn.click(lambda: None, None, chatbot, queue=False)

    return gr.mount_gradio_app(app, blocks.queue(), "/")


app = mount_playground(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
