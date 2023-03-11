from fastapi import FastAPI
from mangum import Mangum

import client
from models import ChatRequest

app = FastAPI()


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.post('/chat')
async def chat(request: ChatRequest):
    res = await client.chat(request.messages)
    return {'result': res}


handler = Mangum(app, lifespan="off")
