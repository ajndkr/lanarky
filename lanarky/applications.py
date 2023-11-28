from typing import Any

from fastapi.applications import AppType, FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse


class Lanarky(FastAPI):
    """The main application class.

    To know more about the FastAPI parameters, read the
    [FastAPI documentation](https://fastapi.tiangolo.com/reference/fastapi/).
    """

    def __init__(
        self: AppType, *, title: str = "Lanarky", **kwargs: dict[str, Any]
    ) -> None:
        """Constructor method.

        Args:
            title: The title of the application.
            **kwargs: Additional arguments to pass to the FastAPI constructor.
        """
        super().__init__(title=title, **kwargs)

    def setup(self) -> None:  # pragma: no cover
        """Setup the application.

        Overrides the `setup` method of the FastAPI class.
        """
        if self.openapi_url:
            urls = (server_data.get("url") for server_data in self.servers)
            server_urls = {url for url in urls if url}

            async def openapi(req: Request) -> JSONResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                if root_path not in server_urls:
                    if root_path and self.root_path_in_servers:
                        self.servers.insert(0, {"url": root_path})
                        server_urls.add(root_path)
                return JSONResponse(self.openapi())

            self.add_route(self.openapi_url, openapi, include_in_schema=False)
        if self.openapi_url and self.docs_url:

            async def swagger_ui_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                oauth2_redirect_url = self.swagger_ui_oauth2_redirect_url
                if oauth2_redirect_url:
                    oauth2_redirect_url = root_path + oauth2_redirect_url
                return get_swagger_ui_html(
                    openapi_url=openapi_url,
                    title=self.title + " - Swagger UI",
                    oauth2_redirect_url=oauth2_redirect_url,
                    init_oauth=self.swagger_ui_init_oauth,
                    swagger_ui_parameters=self.swagger_ui_parameters,
                    swagger_favicon_url="https://lanarky.ajndkr.com/assets/icon.svg",
                )

            self.add_route(self.docs_url, swagger_ui_html, include_in_schema=False)

            if self.swagger_ui_oauth2_redirect_url:

                async def swagger_ui_redirect(req: Request) -> HTMLResponse:
                    return get_swagger_ui_oauth2_redirect_html()

                self.add_route(
                    self.swagger_ui_oauth2_redirect_url,
                    swagger_ui_redirect,
                    include_in_schema=False,
                )
        if self.openapi_url and self.redoc_url:

            async def redoc_html(req: Request) -> HTMLResponse:
                root_path = req.scope.get("root_path", "").rstrip("/")
                openapi_url = root_path + self.openapi_url
                return get_redoc_html(
                    openapi_url=openapi_url,
                    title=self.title + " - ReDoc",
                    redoc_favicon_url="https://lanarky.ajndkr.com/assets/icon.svg",
                )

            self.add_route(self.redoc_url, redoc_html, include_in_schema=False)
