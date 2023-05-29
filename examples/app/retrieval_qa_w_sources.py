from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from lanarky.routing import LangchainRouter
from lanarky.testing import mount_gradio_app

load_dotenv()


def create_chain():
    db = FAISS.load_local(
        folder_path="vector_stores/",
        index_name="langchain-python",
        embeddings=OpenAIEmbeddings(),
    )

    return RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
        ),
        chain_type="stuff",
        retriever=db.as_retriever(),
        return_source_documents=True,
        verbose=True,
    )


app = mount_gradio_app(FastAPI(title="RetrievalQAWithSourcesChainDemo"))
templates = Jinja2Templates(directory="templates")
chain = create_chain()


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


langchain_router = LangchainRouter(
    langchain_url="/chat", langchain_object=chain, streaming_mode=1
)
langchain_router.add_langchain_api_route(
    "/chat_json", langchain_object=chain, streaming_mode=2
)
langchain_router.add_langchain_api_websocket_route("/ws", langchain_object=chain)

app.include_router(langchain_router)
