from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

import pytest
from fastapi import Depends
from langchain.chains import ConversationChain

from lanarky.adapters.langchain.routing import (
    LangchainAPIRoute,
    LangchainAPIRouter,
    LangchainAPIWebSocketRoute,
)


def test_langchain_api_router():
    router = LangchainAPIRouter()

    assert isinstance(router, LangchainAPIRouter)
    assert isinstance(router.routes, list)
    assert router.route_class == LangchainAPIRoute

    with pytest.raises(TypeError):
        router.add_api_websocket_route(
            "/test",
            endpoint=lambda: None,
            name="test_ws_route",
            dependencies=[Depends(lambda: None)],
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
    with pytest.raises(TypeError):
        route = LangchainAPIRoute(
            "/test",
            endpoint=lambda: None,
        )

    route = LangchainAPIRoute(
        "/test",
        endpoint=lambda: create_autospec(ConversationChain),
    )

    assert isinstance(route, LangchainAPIRoute)
    assert route.path == "/test"

    with patch(
        "lanarky.adapters.langchain.routing.build_factory_api_endpoint"
    ) as endpoint_mock:
        endpoint_mock.return_value = AsyncMock()
        LangchainAPIRoute(
            "/test",
            endpoint=lambda: None,
        )
        endpoint_mock.assert_called()

        async def factory_endpoint():
            return MagicMock()

        endpoint_mock.reset_mock()
        LangchainAPIRoute(
            "/test",
            endpoint=factory_endpoint,
        )
        endpoint_mock.assert_not_called()


def test_langchain_websocket_route():
    with patch(
        "lanarky.adapters.langchain.routing.build_factory_websocket_endpoint"
    ) as endpoint_mock:
        endpoint_mock.return_value = AsyncMock()
        LangchainAPIWebSocketRoute(
            "/test",
            endpoint=lambda: None,
        )
        endpoint_mock.assert_called()

        async def factory_endpoint():
            return MagicMock()

        endpoint_mock.reset_mock()
        LangchainAPIWebSocketRoute(
            "/test",
            endpoint=factory_endpoint,
        )
        endpoint_mock.assert_not_called()
