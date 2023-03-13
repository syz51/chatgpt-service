import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from chat import service as chat_service
from chat.model import ChatRequest, ChatResponse
from common.settings import get_environment


@asynccontextmanager
async def lifespan(application):
    get_environment()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.websocket('/chat')
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            request = ChatRequest.parse_obj(await websocket.receive_json())
            await chat_service.chat(request, websocket)
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                status="error",
                message="Sorry, something went wrong. Please try again."
            )
            await websocket.send_json(resp.dict())
