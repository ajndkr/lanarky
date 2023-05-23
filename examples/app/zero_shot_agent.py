from functools import lru_cache
from typing import Callable

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel

from lanarky.responses import StreamingResponse
from lanarky.testing import mount_gradio_app
from lanarky.websockets import WebsocketConnection

load_dotenv()

app = mount_gradio_app(FastAPI(title="ZeroShotAgentDemo"))
templates = Jinja2Templates(directory="templates")


class QueryRequest(BaseModel):
    query: str


def zero_shot_agent_dependency() -> Callable[[], AgentExecutor]:
    @lru_cache(maxsize=1)
    def dependency() -> AgentExecutor:
        llm = ChatOpenAI(
            temperature=0,
            streaming=True,
        )
        tools = load_tools(["llm-math"], llm=llm)
        agent = initialize_agent(
            tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
        )
        return agent

    return dependency


zero_shot_agent = zero_shot_agent_dependency()


@app.post("/chat")
async def chat(
    request: QueryRequest,
    agent: AgentExecutor = Depends(zero_shot_agent),
) -> StreamingResponse:
    return StreamingResponse.from_chain(
        agent, request.query, media_type="text/event-stream"
    )


@app.post("/chat_json")
async def chat_json(
    request: QueryRequest,
    agent: AgentExecutor = Depends(zero_shot_agent),
) -> StreamingResponse:
    return StreamingResponse.from_chain(
        agent, request.query, as_json=True, media_type="text/event-stream"
    )


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, agent: AgentExecutor = Depends(zero_shot_agent)
):
    connection = WebsocketConnection.from_chain(chain=agent, websocket=websocket)
    await connection.connect()
