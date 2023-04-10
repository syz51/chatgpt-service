from fastapi import WebSocket
from langchain import LLMChain
from langchain.callbacks.base import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI

from chat.handler import AsyncChatResponseCallbackHandler
from chat.model import ChatRequest, HumanChatMessage
from config import get_environment, EnvironmentSettings
from db.client import GraphQLClient


async def chat(request: ChatRequest, websocket: WebSocket, client: GraphQLClient):
    settings: EnvironmentSettings = get_environment()
    chat_history = await client.get_messages(request.user_id, request.conversation_id)
    model = ChatOpenAI(openai_api_key=settings.openai_api_key, model_kwargs={'temperature': 0.7},
                       max_retries=1, streaming=True, verbose=True, callback_manager=AsyncCallbackManager(
            [AsyncChatResponseCallbackHandler(conversation_id=request.conversation_id, websocket=websocket,
                                              messages=chat_history + [HumanChatMessage(content=request.message)],
                                              new=len(chat_history) == 0, client=client)]))
    chain = LLMChain(prompt=settings.prompt, llm=model, callback_manager=AsyncCallbackManager(handlers=[]))
    await chain.apredict(input=request.message, history=chat_history)
