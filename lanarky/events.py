from sse_starlette.sse import ServerSentEvent as ServerSentEvent
from sse_starlette.sse import ensure_bytes as ensure_bytes

from lanarky.utils import StrEnum


class Events(StrEnum):
    COMPLETION = "completion"
    ERROR = "error"
    END = "end"
