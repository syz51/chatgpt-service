from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate

from config import get_environment


def generate_prompt(sys_message) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_message),
        HumanMessagePromptTemplate.from_template("{text}")
    ])


def create_chain(prompt: ChatPromptTemplate) -> LLMChain:
    env = get_environment()

    model = ChatOpenAI(openai_api_key=env.openai_api_key, temperature=0, max_retries=1,
                       callback_manager=AsyncCallbackManager(handlers=[]))
    return LLMChain(prompt=prompt, llm=model, callback_manager=AsyncCallbackManager(handlers=[]))
