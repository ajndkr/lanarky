import json

import gradio as gr
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS

from lanarky import Lanarky
from lanarky.adapters.langchain.routing import LangchainAPIRouter
from lanarky.clients import StreamingClient

app = Lanarky()
router = LangchainAPIRouter()


@router.post("/chat")
def chat() -> RetrievalQA:
    db = FAISS.load_local("db/", OpenAIEmbeddings())
    return RetrievalQA.from_chain_type(
        ChatOpenAI(streaming=True),
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
    )


app.include_router(router)


SOURCE_DOCUMENT_TEMPLATE = """
<details><summary><b>Source {idx}</b></summary>{page_content}</details>
"""


def mount_playground(app: Lanarky) -> Lanarky:
    blocks = gr.Blocks(
        title="paulGPT",
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
            history[-1][1] = ""
            for event in StreamingClient().stream_response(
                "POST", "/chat", json={"query": history[-1][0]}
            ):
                if event.event == "completion":
                    history[-1][1] += json.loads(event.data)["token"]
                    yield history
                elif event.event == "source_documents":
                    for idx, document in enumerate(
                        json.loads(event.data)["source_documents"]
                    ):
                        history[-1][1] += SOURCE_DOCUMENT_TEMPLATE.format(
                            idx=idx,
                            page_content=document["page_content"],
                        )
                        yield history
                elif event.event == "error":
                    raise gr.Error(event.data)

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
