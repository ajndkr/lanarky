🔥 Getting Started
===================

.. note::
   Create a `.env` file using `.env.sample` and add your OpenAI API key to it before running the examples.

You can get quickly started with Lanarky and deploy a simple Langchain application in under 20 lines of code:

.. code-block:: python

   from dotenv import load_dotenv
   from fastapi import FastAPI
   from langchain import ConversationChain
   from langchain.chat_models import ChatOpenAI
   from pydantic import BaseModel
   from lanarky.responses import StreamingResponse

   load_dotenv()
   app = FastAPI()

   class Request(BaseModel):
       query: str

   @app.post("/chat")
   async def chat(request: Request) -> StreamingResponse:
       chain = ConversationChain(
        llm=ChatOpenAI(temperature=0, streaming=True), verbose=True
       )
       return StreamingResponse.from_chain(
        chain, request.query, media_type="text/event-stream"
       )

.. image:: https://raw.githubusercontent.com/ajndkr/lanarky/main/assets/demo.gif

.. seealso::
   You can find more Langchain demos in the `examples/ <https://github.com/ajndkr/lanarky/blob/main/examples/README.md>`_ folder of the GitHub repository.
