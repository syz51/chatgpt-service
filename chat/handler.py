from typing import Any, List
from uuid import UUID

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import LLMResult
from pydantic import BaseModel

from chat.model import AIChatMessage
from db.client import GraphQLClient


class AsyncChatResponseCallbackHandler(AsyncCallbackHandler, BaseModel):
    conversation_id: UUID
    websocket: WebSocket
    messages: List
    new: bool
    client: GraphQLClient

    class Config:
        arbitrary_types_allowed = True

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        await self.websocket.send_text(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        conversation_version = self.messages + [AIChatMessage(content=response.generations[0][0].text)]
        if self.new:
            await self.client.create_conversation_version(self.conversation_id, conversation_version)
        else:
            await self.client.update_conversation_version(self.conversation_id, conversation_version)
        await self.websocket.send_text(data="data: [DONE]")
