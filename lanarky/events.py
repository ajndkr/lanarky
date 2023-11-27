from enum import Enum

from sse_starlette.sse import ServerSentEvent as ServerSentEvent
from sse_starlette.sse import ensure_bytes as ensure_bytes


class Events(str, Enum):
    COMPLETION = "completion"
    ERROR = "error"
    END = "end"
