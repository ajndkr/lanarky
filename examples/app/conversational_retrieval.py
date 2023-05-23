from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from lanarky.responses import StreamingResponse
from lanarky.testing import mount_gradio_app

load_dotenv()

app = mount_gradio_app(FastAPI(title="ConversationalRetrievalChainDemo"))

templates = Jinja2Templates(directory="templates")


class QueryRequest(BaseModel):
    query: str
    history: list[list[str]] = []


def conversational_retrieval_chain_dependency() -> (
    Callable[[], ConversationalRetrievalChain]
):
    @lru_cache(maxsize=1)
    def dependency() -> ConversationalRetrievalChain:
        from langchain.chains.conversational_retrieval.prompts import (
            CONDENSE_QUESTION_PROMPT,
        )
        from langchain.embeddings import OpenAIEmbeddings
        from langchain.vectorstores import FAISS

        db = FAISS.load_local(
            folder_path="vector_stores/",
            index_name="langchain-python",
            embeddings=OpenAIEmbeddings(),
        )

        question_generator = LLMChain(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
            ),
            prompt=CONDENSE_QUESTION_PROMPT,
        )
        doc_chain = load_qa_chain(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
            ),
            chain_type="stuff",
        )

        return ConversationalRetrievalChain(
            combine_docs_chain=doc_chain,
            question_generator=question_generator,
            retriever=db.as_retriever(),
            return_source_documents=True,
            verbose=True,
        )

    return dependency


conversational_retrieval_chain = conversational_retrieval_chain_dependency()


@app.post("/chat")
async def chat(
    request: QueryRequest,
    chain: ConversationalRetrievalChain = Depends(conversational_retrieval_chain),
) -> StreamingResponse:
    inputs = {
        "question": request.query,
        "chat_history": [(human, ai) for human, ai in request.history],
    }
    return StreamingResponse.from_chain(chain, inputs, media_type="text/event-stream")


@app.post("/chat_json")
async def chat_json(
    request: QueryRequest,
    chain: ConversationalRetrievalChain = Depends(conversational_retrieval_chain),
) -> StreamingResponse:
    return StreamingResponse.from_chain(
        chain, request.query, as_json=True, media_type="text/event-stream"
    )
