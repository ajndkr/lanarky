import pytest
from fastapi.testclient import TestClient

from lanarky import Lanarky


@pytest.fixture
def app() -> Lanarky:
    return Lanarky()


def test_app_instance(app: Lanarky):
    assert isinstance(app, Lanarky)
    assert app.title == "Lanarky"


def test_custom_title():
    custom_title = "My Custom Title"
    app = Lanarky(title=custom_title)
    assert app.title == custom_title


def test_app_routes(app: Lanarky):
    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 404
