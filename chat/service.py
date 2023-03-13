from langchain.chains import ConversationChain

from chat.memory import DynamodbChatMemory
from chat.model import ChatRequest
from chat.settings import ChatSettings, get_chat_settings


async def chat(chat_request: ChatRequest, settings: ChatSettings = get_chat_settings()) -> str:
    memory = DynamodbChatMemory(chat_id=chat_request.chat_id)
    conversation = ConversationChain(memory=memory, prompt=settings.prompt, llm=settings.model)
    return await conversation.apredict(input=chat_request.message)
