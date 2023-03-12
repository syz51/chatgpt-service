from typing import List, Literal

from dyntastic import Dyntastic
from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    chat_id: str
    message: str


class ChatResponse(BaseModel):
    message: str


class AIChatMessage(AIMessage):
    type: Literal['AI'] = 'AI'


class HumanChatMessage(HumanMessage):
    type: Literal['Human'] = 'Human'


class ChatHistory(Dyntastic):
    __table_name__ = "chatgpt-messages"
    __hash_key__ = "chat_id"
    __table_region__ = 'ap-east-1'

    chat_id: str
    messages: List[AIChatMessage | HumanChatMessage] = Field(default_factory=list)

    def add_user_message(self, message: str) -> None:
        self.messages.append(HumanChatMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.messages.append(AIChatMessage(content=message))

    def clear(self) -> None:
        self.delete()
