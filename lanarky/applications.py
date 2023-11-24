from typing import Any

from fastapi.applications import AppType, FastAPI


class Lanarky(FastAPI):
    """The main application class.

    To know more about the FastAPI parameters, read the FastAPI documentation:
    https://fastapi.tiangolo.com/reference/fastapi/
    """

    def __init__(self: AppType, *, title: str = "Lanarky", **kwargs: Any) -> None:
        super().__init__(title=title, **kwargs)
