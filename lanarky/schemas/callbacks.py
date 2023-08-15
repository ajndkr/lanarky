from typing import Any

from pydantic import BaseModel


class StreamingJSONResponse(BaseModel):
    """Streaming JSON response."""

    token: str = ""


class AnswerStreamingJSONResponse(BaseModel):
    """Answer response used when cache is enabled and tokens haven't been streamed.
    Should only be output when on_llm_new_token hasn't been invoked before on_chain_end.
    """

    answer: str = ""  # only returned when langchain.llm_cache is used


class BaseRetrievalQAStreamingJSONResponse(BaseModel):
    """Base class for retrieval-based QA streaming JSON response."""

    source_documents: list[dict[str, Any]]
