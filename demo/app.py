from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from langchain import ConversationChain
from langchain.callbacks import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from fastapi_async_langchain.responses import LLMChainStreamingResponse, RetrievalQAStreamingResponse

load_dotenv()

app = FastAPI(title="StreamingConversationChainAPI")


class Request(BaseModel):
    query: str


def conversation_chain_dependency() -> Callable[[], ConversationChain]:
    @lru_cache(maxsize=1)
    def dependency() -> ConversationChain:
        return ConversationChain(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
                callback_manager=AsyncCallbackManager([]),
            ),
            verbose=True,
        )

    return dependency


conversation_chain = conversation_chain_dependency()


@app.post("/chat")
async def chat(
    request: Request,
    chain: ConversationChain = Depends(conversation_chain),
) -> LLMChainStreamingResponse:
    return LLMChainStreamingResponse(
        chain, request.query, media_type="text/event-stream"
    )

def retrieval_qa_chain():
    from langchain.chains import RetrievalQAWithSourcesChain
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain
    from langchain.chains.qa_with_sources.stuff_prompt import PROMPT as QA_PROMPT
    from langchain.vectorstores import FAISS
    from langchain.embeddings import OpenAIEmbeddings

    callback_manager = AsyncCallbackManager([])
    vectorstore = FAISS.load_local(index_name="langchain-python", embeddings=OpenAIEmbeddings(), folder_path="demo/")
    retriever = vectorstore.as_retriever()
    streaming_llm = ChatOpenAI(streaming=True, callback_manager=callback_manager, verbose=True, temperature=0)
    doc_chain = load_qa_with_sources_chain(llm=streaming_llm,
                                           chain_type="stuff",
                                           prompt=QA_PROMPT)
    return RetrievalQAWithSourcesChain(combine_documents_chain=doc_chain,
                                       retriever=retriever,
                                       callback_manager=callback_manager,
                                       return_source_documents=True,
                                       verbose=True)

@app.post("/retrieval-qa-with-sources")
async def retrieval_qa_with_sources(
    request: Request
) -> RetrievalQAStreamingResponse:
    return RetrievalQAStreamingResponse(
        chain=retrieval_qa_chain(),
        inputs=request.query,
        media_type="text/event-stream"
    )
