from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from langchain.agents import AgentExecutor, AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI

from lanarky.routing import LangchainRouter
from lanarky.testing import mount_gradio_app

load_dotenv()


def create_chain() -> AgentExecutor:
    llm = ChatOpenAI(
        temperature=0,
        streaming=True,
    )
    tools = load_tools(["llm-math"], llm=llm)
    return initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )


app = mount_gradio_app(FastAPI(title="ZeroShotAgentDemo"))
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
