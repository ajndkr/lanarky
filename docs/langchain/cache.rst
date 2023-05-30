Deploy Applications with LLM Caching
=====================================

Langchain offers multiple LLM cache solutions. Reference: `How to cache LLM calls <https://python.langchain.com/en/latest/modules/models/llms/examples/llm_caching.html>`_

To simplify the use of these solutions for Lanarky users, the ``LangchainRouter`` can be used to setup LLM caching for your application.

We'll use a simple ``LLMChain`` application as an example:

.. code-block:: python

    from dotenv import load_dotenv
    from fastapi import FastAPI
    from langchain import LLMChain
    from langchain.llms import OpenAI

    from lanarky import LangchainRouter

    load_dotenv()

    app = FastAPI()

    langchain_router = LangchainRouter(
        langchain_url="/chat",
        langchain_object=LLMChain.from_string(
            llm=OpenAI(temperature=0), template="Answer the query.\n{query}"
        ),
        streaming_mode=0,
    )

    app.include_router(langchain_router)

The ``LangchainRouter`` class uses the ``llm_cache_mode`` parameter to setup LLM caching.
There are three available modes:

- ``llm_cache_mode=0``: No LLM caching
- ``llm_cache_mode=1``: In-memory LLM caching
- ``llm_cache_mode=2``: Redis LLM caching
- ``llm_cache_mode=3``: GPTCache LLM caching

In-Memory Caching
-----------------

To setup in-memory caching, use the following ``LangchainRouter`` configuration:

.. code-block:: python

    langchain_router = LangchainRouter(
        langchain_url="/chat",
        langchain_object=LLMChain.from_string(
            llm=OpenAI(temperature=0), template="Answer the query.\n{query}"
        ),
        streaming_mode=0,
        llm_cache_mode=1,
    )


Redis Caching
-------------

To setup Redis caching, first install the required dependencies:

.. code-block:: bash

    pip install "lanarky[redis]"

Next, setup a Redis server. We recommend using Docker:

.. code-block:: bash

    docker run --name redis -p 6379:6379 -d redis

Finally, use the following ``LangchainRouter`` configuration:

.. code-block:: python

    langchain_router = LangchainRouter(
        langchain_url="/chat",
        langchain_object=LLMChain.from_string(
            llm=OpenAI(temperature=0), template="Answer the query.\n{query}"
        ),
        streaming_mode=0,
        llm_cache_mode=2,
        llm_cache_kwargs={"url": "redis://localhost:6379/"},
    )


GPTCache Caching
----------------

To setup GPTCache caching, first install the required dependencies:

.. code-block:: bash

    pip install "lanarky[gptcache]"

Then, use the following ``LangchainRouter`` configuration:

.. code-block:: python

    langchain_router = LangchainRouter(
        langchain_url="/chat",
        langchain_object=LLMChain.from_string(
            llm=OpenAI(temperature=0), template="Answer the query.\n{query}"
        ),
        streaming_mode=0,
        llm_cache_mode=3,
    )
