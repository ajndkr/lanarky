from unittest.mock import create_autospec

import pytest
from langchain.chains import ConversationChain

from lanarky.adapters.langchain.routing import LangchainAPIRoute, LangchainAPIRouter


def test_langchain_api_router():
    router = LangchainAPIRouter()

    assert isinstance(router, LangchainAPIRouter)
    assert isinstance(router.routes, list)
    assert router.route_class == LangchainAPIRoute

    def mock_endpoint():
        pass

    with pytest.raises(TypeError):
        router.add_api_websocket_route(
            "/test",
            endpoint=mock_endpoint,
            name="test_ws_route",
        )

    def mock_chain_factory():
        return create_autospec(ConversationChain)

    router.add_api_websocket_route(
        "/test",
        endpoint=mock_chain_factory,
        name="test_ws_route",
    )

    assert len(router.routes) == 1
    assert router.routes[0].path == "/test"
    assert router.routes[0].name == "test_ws_route"


def test_langchain_api_route():
    def mock_endpoint():
        pass

    with pytest.raises(TypeError):
        route = LangchainAPIRoute(
            "/test",
            endpoint=mock_endpoint,
        )

    def mock_chain_factory():
        return create_autospec(ConversationChain)

    route = LangchainAPIRoute(
        "/test",
        endpoint=mock_chain_factory,
    )

    assert isinstance(route, LangchainAPIRoute)
    assert route.path == "/test"
