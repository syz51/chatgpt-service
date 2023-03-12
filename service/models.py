from typing import List, Literal, Union

from dyntastic import Dyntastic
from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel, Field

from service.settings import get_environment


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
    __table_name__ = get_environment().table_name
    __hash_key__ = "chat_id"
    __table_region__ = get_environment().aws_region

    chat_id: str
    messages: List[Union[AIChatMessage, HumanChatMessage]] = Field(default_factory=list)

    def add_user_message(self, message: str) -> None:
        self.messages.append(HumanChatMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.messages.append(AIChatMessage(content=message))

    def clear(self) -> None:
        self.delete()
