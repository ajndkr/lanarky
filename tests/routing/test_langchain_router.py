from unittest.mock import MagicMock

import pytest
from langchain.chains import ConversationChain

from lanarky.routing import LangchainRouter, LLMCacheMode


@pytest.fixture
def chain():
    return MagicMock(spec=ConversationChain)


def test_langchain_router_init():
    router = LangchainRouter()

    assert router.langchain_object is None
    assert router.streaming_mode is None
    assert router.langchain_url is None
    assert router.langchain_endpoint_kwargs == {}
    assert router.langchain_dependencies == []
    assert router.llm_cache_mode is None
    assert router.llm_cache_kwargs == {}


def test_langchain_router_add_routes(chain):
    with pytest.raises(ValueError):
        LangchainRouter(langchain_url="/chat", langchain_object=chain, streaming_mode=3)

    router = LangchainRouter()

    router.add_langchain_api_route(
        url="/chat", langchain_object=chain, streaming_mode=0
    )

    assert len(router.routes) == 1
    assert router.routes[0].methods == {"POST"}
    assert router.routes[0].path == "/chat"
    assert "LangchainResponse" in router.routes[0].response_model.schema()["title"]
    assert "LangchainRequest" in router.routes[0].body_field.type_.schema()["title"]

    router.add_langchain_api_route(
        url="/chat", langchain_object=chain, streaming_mode=1
    )

    assert len(router.routes) == 2
    assert router.routes[1].methods == {"POST"}
    assert router.routes[1].path == "/chat"
    assert router.routes[1].response_model is None
    assert "LangchainRequest" in router.routes[1].body_field.type_.schema()["title"]

    router.add_langchain_api_route(
        url="/chat", langchain_object=chain, streaming_mode=2
    )

    assert len(router.routes) == 3
    assert router.routes[2].methods == {"POST"}
    assert router.routes[2].path == "/chat"
    assert router.routes[2].response_model is None
    assert "LangchainRequest" in router.routes[2].body_field.type_.schema()["title"]


def test_langchain_router_enable_llm_cache(chain):
    router = LangchainRouter(
        langchain_url="/chat",
        langchain_object=chain,
        streaming_mode=0,
        llm_cache_mode=1,
    )

    assert router.llm_cache_mode == LLMCacheMode.IN_MEMORY

    import langchain

    assert langchain.llm_cache is not None
