import random
import string
from typing import Any, Optional, Type

from fastapi.routing import APIRouter
from fastapi.websockets import WebSocket
from langchain.chains.base import Chain

from .utils import (
    LLMCacheMode,
    StreamingMode,
    create_langchain_dependency,
    create_langchain_endpoint,
    create_langchain_websocket_endpoint,
    create_request_from_langchain_dependency,
    create_response_model_from_langchain_dependency,
)


class LangchainRouter(APIRouter):
    def __init__(
        self,
        *,
        langchain_url: Optional[str] = None,
        langchain_object: Optional[Type[Chain]] = None,
        langchain_endpoint_kwargs: Optional[dict[str, Any]] = None,
        streaming_mode: Optional[StreamingMode] = None,
        llm_cache_mode: Optional[LLMCacheMode] = None,
        llm_cache_kwargs: Optional[dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.langchain_url = langchain_url
        self.langchain_object = langchain_object
        self.langchain_endpoint_kwargs = langchain_endpoint_kwargs or {}
        self.streaming_mode = streaming_mode
        self.llm_cache_mode = llm_cache_mode
        self.llm_cache_kwargs = llm_cache_kwargs or {}

        self.langchain_dependencies = []

        self.setup()

    def setup(self) -> None:
        """Sets up the Langchain router."""
        if self.langchain_url is not None:
            self.add_langchain_api_route(
                self.langchain_url,
                self.langchain_object,
                self.streaming_mode,
                **self.langchain_endpoint_kwargs,
            )

        if self.llm_cache_mode is not None:
            self.setup_llm_cache()

    def setup_llm_cache(self) -> None:
        """Sets up the LLM cache."""
        import langchain

        if self.llm_cache_mode == LLMCacheMode.IN_MEMORY:
            from langchain.cache import InMemoryCache

            langchain.llm_cache = InMemoryCache()

        elif self.llm_cache_mode == LLMCacheMode.REDIS:
            try:
                from redis import Redis  # type: ignore
            except ImportError:
                raise ImportError(
                    """Redis is not installed. Install it with `pip install "lanarky[redis]"`."""
                )
            from langchain.cache import RedisCache

            langchain.llm_cache = RedisCache(
                redis_=Redis.from_url(**self.llm_cache_kwargs)
            )

        elif self.llm_cache_mode == LLMCacheMode.GPTCACHE:
            try:
                from gptcache import Cache  # type: ignore
                from gptcache.manager.factory import manager_factory  # type: ignore
                from gptcache.processor.pre import get_prompt  # type: ignore
            except ImportError:
                raise ImportError(
                    """GPTCache is not installed. Install it with `pip install "lanarky[gptcache]"`."""
                )
            import hashlib

            from langchain.cache import GPTCache

            def init_gptcache(cache_obj: Cache, llm: str):
                hashed_llm = hashlib.sha256(llm.encode()).hexdigest()
                cache_obj.init(
                    pre_embedding_func=get_prompt,
                    data_manager=manager_factory(
                        manager="map", data_dir=f"map_cache_{hashed_llm}"
                    ),
                )

            langchain.llm_cache = GPTCache(init_gptcache)

        else:
            raise ValueError(f"Invalid LLM cache mode: {self.llm_cache_mode}")

    def add_langchain_api_route(
        self,
        url: str,
        langchain_object: Chain,
        streaming_mode: StreamingMode,
        methods: list[str] = ["POST"],
        **kwargs,
    ):
        """Adds a Langchain API route to the router."""
        langchain_dependency = create_langchain_dependency(langchain_object)

        name_prefix = "".join(
            random.choice(string.ascii_letters) for _ in range(5)
        ).title()
        endpoint_request = create_request_from_langchain_dependency(
            langchain_dependency, name_prefix
        )
        response_model = (
            create_response_model_from_langchain_dependency(
                langchain_dependency, name_prefix
            )
            if streaming_mode == StreamingMode.OFF
            else None
        )

        endpoint = create_langchain_endpoint(
            endpoint_request,
            langchain_dependency,
            response_model,
            streaming_mode,
        )

        self.add_api_route(
            url,
            endpoint,
            response_model=response_model,
            methods=methods,
            **kwargs,
        )

        self.langchain_dependencies.append(langchain_dependency)

    def add_langchain_api_websocket_route(self, url: str, langchain_object: Chain):
        """Adds a Langchain API websocket route to the router."""
        langchain_dependency = create_langchain_dependency(langchain_object)
        endpoint = create_langchain_websocket_endpoint(
            WebSocket,
            langchain_dependency,
        )

        self.add_api_websocket_route(url, endpoint)

        self.langchain_dependencies.append(langchain_dependency)
