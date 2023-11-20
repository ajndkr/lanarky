from typing import Any

from llama_index.indices.base import BaseIndex

from lanarky.responses import StreamingResponse as _StreamingResponse


class StreamingResponse(_StreamingResponse):
    def __init__(
        self,
        index: BaseIndex,
        query: str,
        query_engine_kwargs: dict[str, Any],
        *args,
        **kwargs,
    ) -> None:
        query_engine = index.as_query_engine(streaming=True, **query_engine_kwargs)
        content = query_engine.query(query).response_gen

        super().__init__(content=content, *args, **kwargs)
