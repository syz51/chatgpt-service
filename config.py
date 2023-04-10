from functools import lru_cache
from typing import Any

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from pydantic import BaseSettings, Field


class EnvironmentSettings(BaseSettings):
    openai_api_key: str
    allowed_origin: str
    db_url: str
    db_key: str

    sys_message = "The following is a friendly conversation between a human and an AI. The AI is talkative and " \
                  "provides lots of specific details from its context. If the AI does not know the answer to a " \
                  "question, it truthfully says it does not know."
    prompt: Any = Field(default=None)

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_environment() -> EnvironmentSettings:
    env = EnvironmentSettings()
    env.prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(env.sys_message),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    return env
