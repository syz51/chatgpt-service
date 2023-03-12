from functools import lru_cache

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from pydantic import BaseSettings, BaseModel


class EnvironmentSettings(BaseSettings):
    openai_api_key: str
    aws_region: str
    table_name: str

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_environment() -> EnvironmentSettings:
    return EnvironmentSettings()


class ChatSettings(BaseModel):
    sys_message = "The following is a friendly conversation between a human and an AI. The AI is talkative and " \
                  "provides lots of specific details from its context. The AI is called ChatGPT, a large language " \
                  "model trained by OpenAI. If the AI does not know the answer to a question, it truthfully says it " \
                  "does not know."
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_message),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    model = ChatOpenAI(openai_api_key=get_environment().openai_api_key, model_kwargs={'temperature': 0.7})


@lru_cache(maxsize=1)
def get_chat_settings() -> ChatSettings:
    return ChatSettings()
