from unittest.mock import MagicMock

import pytest
from fastapi.params import Depends
from langchain.chains import ConversationChain

from lanarky.routing import LangchainRouter


@pytest.fixture
def chain():
    return MagicMock(spec=ConversationChain)


def test_langchain_router_init(chain):
    router = LangchainRouter(langchain_object=chain)

    assert router.langchain_object == chain
    assert router.streaming_mode == 0
    assert router.langchain_url == "/chat"
    assert router.langchain_endpoint_kwargs == {}
    assert isinstance(router.langchain_dependency, Depends)

    with pytest.raises(ValueError):
        LangchainRouter(langchain_object=chain, streaming_mode=3)


def test_langchain_router_base_route(chain):
    router = LangchainRouter(langchain_object=chain)

    assert len(router.routes) == 1
    assert router.routes[0].methods == {"POST"}
    assert router.routes[0].path == "/chat"
    assert router.routes[0].response_model.schema()["title"] == "LangchainResponse"
    assert router.routes[0].body_field.type_.schema()["title"] == "LangchainRequest"


def test_langchain_router_streaming_route(chain):
    router = LangchainRouter(langchain_object=chain, streaming_mode=1)

    assert len(router.routes) == 1
    assert router.routes[0].methods == {"POST"}
    assert router.routes[0].path == "/chat"
    assert router.routes[0].response_model is None
    assert router.routes[0].body_field.type_.schema()["title"] == "LangchainRequest"


def test_langchain_router_streaming_json_route(chain):
    router = LangchainRouter(langchain_object=chain, streaming_mode=2)

    assert len(router.routes) == 1
    assert router.routes[0].methods == {"POST"}
    assert router.routes[0].path == "/chat"
    assert router.routes[0].response_model is None
    assert router.routes[0].body_field.type_.schema()["title"] == "LangchainRequest"
