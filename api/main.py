from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from langchain import LLMChain
from pydantic import BaseModel
from starlette.types import Send

from .chain import load_conversation_chain
from .response import LangchainStreamingResponse

load_dotenv()

app = FastAPI(title="LangchainAPI")


class Request(BaseModel):
    query: str


def conversation_chain_dependency() -> Callable[[], LLMChain]:
    @lru_cache(maxsize=1)
    def dependency() -> LLMChain:
        return load_conversation_chain()

    return dependency


conversation_chain = conversation_chain_dependency()


@app.post("/chat")
async def chat(
    request: Request,
    chain: LLMChain = Depends(conversation_chain),
):
    def llm_chain_wrapper_fn(question: str, chain: LLMChain) -> Callable:
        async def wrapper(send: Send):
            chain.llm.callback_manager.handlers[0].send = send
            await chain.arun(question)

        return wrapper

    return LangchainStreamingResponse(
        llm_chain_wrapper_fn(request.query, chain), media_type="text/event-stream"
    )
