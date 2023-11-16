from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str = "Chatbot Playground"

    # gradio settings
    api_url: str = "http://localhost:8000"
    api_endpoint: str = "/chat"
    gradio_path: str = "/gradio"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
