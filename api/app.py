from fastapi import FastAPI

from service import client
from service.models import ChatRequest, ChatResponse

app = FastAPI()


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.post('/chat')
async def chat(request: ChatRequest):
    return ChatResponse(message=await client.chat(request))
