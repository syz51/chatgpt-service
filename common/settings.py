from functools import lru_cache

from pydantic import BaseSettings


class EnvironmentSettings(BaseSettings):
    openai_api_key: str
    aws_region: str
    table_name: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_environment() -> EnvironmentSettings:
    return EnvironmentSettings()
