from functools import lru_cache

from pydantic import BaseSettings


class EnvironmentSettings(BaseSettings):
    openai_api_key: str
    aws_region: str
    table_name: str
    allowed_origin: str

    sys_message = "The following is a friendly conversation between a human and an AI. The AI is talkative and " \
                  "provides lots of specific details from its context. If the AI does not know the answer to a " \
                  "question, it truthfully says it does not know."

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_environment() -> EnvironmentSettings:
    return EnvironmentSettings()
