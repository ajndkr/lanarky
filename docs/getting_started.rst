🔥 Getting Started
===================

.. note::
   Create a `.env` file using `.env.sample` and add your OpenAI API key to it before running the examples.

You can get quickly started with Lanarky and deploy your first Langchain app in just a few lines of code.

.. code-block:: python

   from dotenv import load_dotenv
   from fastapi import FastAPI
   from langchain import ConversationChain
   from langchain.chat_models import ChatOpenAI

   from lanarky import LangchainRouter

   load_dotenv()
   app = FastAPI()

   langchain_router = LangchainRouter(
      langchain_url="/chat",
      langchain_object=ConversationChain(
         llm=ChatOpenAI(temperature=0), verbose=True
      ),
      streaming_mode=0
   )
   app.include_router(langchain_router)

.. image:: https://raw.githubusercontent.com/ajndkr/lanarky/main/assets/demo.gif

.. seealso::
   You can find more LangChain demos in the `examples/ <https://github.com/ajndkr/lanarky/blob/main/examples/README.md>`_
   folder of the GitHub repository.
