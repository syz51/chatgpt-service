from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackManager
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, \
    ChatPromptTemplate

from chat.handler import AsyncChatResponseCallbackHandler
from chat.memory import DynamodbChatMemory
from chat.model import ChatRequest
from common.settings import get_environment, EnvironmentSettings


async def chat(chat_request: ChatRequest, websocket: WebSocket,
               settings: EnvironmentSettings = get_environment()) -> str:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(settings.sys_message),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    memory = DynamodbChatMemory(chat_id=chat_request.chat_id)
    model = ChatOpenAI(openai_api_key=settings.openai_api_key, model_kwargs={'temperature': 0.7},
                       max_retries=1, streaming=True, verbose=True, callback_manager=AsyncCallbackManager(
            [AsyncChatResponseCallbackHandler(chat_id=chat_request.chat_id, websocket=websocket)]))

    conversation = ConversationChain(memory=memory, prompt=prompt, llm=model)
    return await conversation.apredict(input=chat_request.message)
