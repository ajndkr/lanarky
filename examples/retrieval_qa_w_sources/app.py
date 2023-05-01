from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from langchain.callbacks import AsyncCallbackManager
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from fastapi_async_langchain.gradio import mount_gradio_app
from fastapi_async_langchain.responses import RetrievalQAStreamingResponse

load_dotenv()

app = mount_gradio_app(FastAPI(title="RetrievalQAWithSourcesChainDemo"))


class Request(BaseModel):
    query: str


def retrieval_qa_chain_dependency() -> Callable[[], RetrievalQAWithSourcesChain]:
    @lru_cache(maxsize=1)
    def dependency() -> RetrievalQAWithSourcesChain:
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS

        db = FAISS.load_local(
            folder_path="vector_stores/",
            index_name="langchain-python",
            embeddings=OpenAIEmbeddings(),
        )

        return RetrievalQAWithSourcesChain.from_chain_type(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
                callback_manager=AsyncCallbackManager([]),
            ),
            chain_type="stuff",
            retriever=db.as_retriever(),
            return_source_documents=True,
            verbose=True,
        )

    return dependency


retrieval_qa_chain = retrieval_qa_chain_dependency()


@app.post("/chat")
async def chat(
    request: Request,
    chain: RetrievalQAWithSourcesChain = Depends(retrieval_qa_chain),
) -> RetrievalQAStreamingResponse:
    return RetrievalQAStreamingResponse.from_chain(
        chain, request.query, media_type="text/event-stream"
    )
