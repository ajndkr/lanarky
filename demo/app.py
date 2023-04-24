from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from langchain import ConversationChain
from langchain.callbacks import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from fastapi_async_langchain.responses import LLMChainStreamingResponse

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
