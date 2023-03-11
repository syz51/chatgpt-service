from functools import lru_cache

from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        env_file = "../.env"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


class ChatRequest(BaseModel):
    messages: list
