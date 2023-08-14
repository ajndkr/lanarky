from typing import Any

from pydantic import BaseModel


class StreamingJSONResponse(BaseModel):
    """Streaming JSON response."""

    token: str = ""
    answer: str = ""  # only returned when langchain.llm_cache is used


class BaseRetrievalQAStreamingJSONResponse(StreamingJSONResponse):
    """Base class for retrieval-based QA streaming JSON response."""

    source_documents: list[dict[str, Any]]
