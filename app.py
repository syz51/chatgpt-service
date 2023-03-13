from contextlib import asynccontextmanager

from fastapi import FastAPI

from chat import service as chat_service
from chat.settings import get_chat_settings
from chat.model import ChatRequest, ChatResponse


@asynccontextmanager
async def lifespan(application: FastAPI):
    get_chat_settings()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.post('/chat')
async def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(message=await chat_service.chat(request))
