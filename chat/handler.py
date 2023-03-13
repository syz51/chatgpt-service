from typing import Any

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import LLMResult
from pydantic import BaseModel


class AsyncChatResponseCallbackHandler(AsyncCallbackHandler, BaseModel):
    chat_id: str
    websocket: WebSocket

    class Config:
        arbitrary_types_allowed = True

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        await self.websocket.send_text(token)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        await self.websocket.send_text(data="data: [DONE]")
