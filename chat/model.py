from typing import Literal
from uuid import UUID

from langchain.schema import HumanMessage, AIMessage
from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: UUID
    user_id: UUID
    message: str


class ChatResponse(BaseModel):
    message: str
    status: str


class MessagesRequest(BaseModel):
    user_id: UUID
    conversation_id: UUID


class ConversationsRequest(BaseModel):
    user_id: UUID


class AIChatMessage(AIMessage):
    message_type: Literal['AI'] = 'AI'


class HumanChatMessage(HumanMessage):
    message_type: Literal['Human'] = 'Human'
