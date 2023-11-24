from unittest.mock import create_autospec

import pytest

from lanarky.adapters.openai.resources import ChatCompletionResource
from lanarky.adapters.openai.routing import OpenAIAPIRoute, OpenAIAPIRouter


def test_langchain_api_router():
    router = OpenAIAPIRouter()

    assert isinstance(router, OpenAIAPIRouter)
    assert isinstance(router.routes, list)
    assert router.route_class == OpenAIAPIRoute

    def mock_endpoint():
        pass

    with pytest.raises(TypeError):
        router.add_api_websocket_route(
            "/test",
            endpoint=mock_endpoint,
            name="test_ws_route",
        )

    def mock_chain_factory():
        return create_autospec(ChatCompletionResource)

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
        route = OpenAIAPIRoute(
            "/test",
            endpoint=mock_endpoint,
        )

    def mock_chain_factory():
        return create_autospec(ChatCompletionResource)

    route = OpenAIAPIRoute(
        "/test",
        endpoint=mock_chain_factory,
    )

    assert isinstance(route, OpenAIAPIRoute)
    assert route.path == "/test"
