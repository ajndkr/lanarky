from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = "Chatbot Playground"

    # gradio settings
    api_url: str = "http://localhost:8000"
    api_endpoint: str = "/chat"
    gradio_path: str = "/gradio"

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
