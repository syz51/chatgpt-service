from functools import lru_cache

from langchain.callbacks.base import AsyncCallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from pydantic import BaseModel

from common.settings import get_environment


class ChatSettings(BaseModel):
    sys_message = "The following is a friendly conversation between a human and an AI. The AI is talkative and " \
                  "provides lots of specific details from its context. If the AI does not know the answer to a " \
                  "question, it truthfully says it does not know."
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_message),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    model = ChatOpenAI(openai_api_key=get_environment().openai_api_key, model_kwargs={'temperature': 0.7},
                       max_retries=1, streaming=True, verbose=True,
                       callback_manager=AsyncCallbackManager([StreamingStdOutCallbackHandler()]))


@lru_cache(maxsize=1)
def get_chat_settings() -> ChatSettings:
    return ChatSettings()
