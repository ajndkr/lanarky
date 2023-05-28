Deploying Langchain Applications
=================================

Lanarky offers a straightforward method for deploying your Langchain app using ``LangchainRouter``.

``LangchainRouter`` inherits from FastAPI's ``APIRouter`` class and creates an API endpoint using your target Langchain object.

To better understand ``LangchainRouter``, let's break down the example below:

.. code-block:: python

    from dotenv import load_dotenv
    from fastapi import FastAPI
    from langchain import ConversationChain
    from langchain.chat_models import ChatOpenAI
    from lanarky.routing import LangchainRouter

    load_dotenv()
    app = FastAPI()

    langchain_router = LangchainRouter(
        langchain_object=ConversationChain(
            llm=ChatOpenAI(temperature=0),
            verbose=True
        )
    )
    app.include_router(langchain_router)

In the above example, ``langchain_router`` is an instance of the ``APIRouter`` class that creates a POST endpoint at ``/chat``.
This endpoint accepts JSON data as input and returns JSON data as output.

Now, let's explore an interesting feature of Lanarky - the ability to deploy your Langchain app with token streaming.
Here's an example:

.. code-block:: python

    from dotenv import load_dotenv
    from fastapi import FastAPI
    from langchain import ConversationChain
    from langchain.chat_models import ChatOpenAI
    from lanarky.routing import LangchainRouter

    load_dotenv()
    app = FastAPI()

    langchain_router = LangchainRouter(
        langchain_object=ConversationChain(
            llm=ChatOpenAI(temperature=0, streaming=True),
            verbose=True
        ),
        streaming_mode=1
    )
    app.include_router(langchain_router)

By including ``streaming_mode=1`` in the ``LangchainRouter`` initialization, your Langchain app can be deployed
with token streaming.

The ``LangchainRouter`` class uses the ``streaming_mode`` parameter to determine the token streaming behavior.
There are three available modes:

- ``streaming_mode=0``: No token streaming
- ``streaming_mode=1``: Token streaming as plain text
- ``streaming_mode=2``: Token streaming as JSON
