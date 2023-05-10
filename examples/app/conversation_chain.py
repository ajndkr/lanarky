from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from fastapi_async_langchain.responses import LLMChainStreamingResponse
from fastapi_async_langchain.testing import mount_gradio_app
from fastapi_async_langchain.websockets import LLMChainWebsocketConnection

load_dotenv()

app = mount_gradio_app(FastAPI(title="ConversationChainDemo"))
templates = Jinja2Templates(directory="templates")


class QueryRequest(BaseModel):
    query: str


def conversation_chain_dependency() -> Callable[[], ConversationChain]:
    @lru_cache(maxsize=1)
    def dependency() -> ConversationChain:
        return ConversationChain(
            llm=ChatOpenAI(
                temperature=0,
                streaming=True,
            ),
            verbose=True,
        )

    return dependency


conversation_chain = conversation_chain_dependency()


@app.post("/chat")
async def chat(
    request: QueryRequest,
    chain: ConversationChain = Depends(conversation_chain),
) -> LLMChainStreamingResponse:
    return LLMChainStreamingResponse.from_chain(
        chain, request.query, media_type="text/event-stream"
    )


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, chain: ConversationChain = Depends(conversation_chain)
):
    connection = LLMChainWebsocketConnection.from_chain(
        chain=chain, websocket=websocket
    )
    await connection.connect()
