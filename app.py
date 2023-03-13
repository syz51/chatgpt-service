import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from chat import service as chat_service
from chat.model import ChatRequest, ChatResponse, MessagesRequest, ChatHistory
from common.settings import get_environment


@asynccontextmanager
async def lifespan(application):
    get_environment()
    yield


app = FastAPI(lifespan=lifespan, openapi_url=None)


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.post('/messages')
async def messages(request: MessagesRequest) -> ChatHistory:
    return await chat_service.get_history_messages(chat_id=request.chat_id)


@app.get('/chat/list')
async def chat_list():
    return await chat_service.list_chat_ids()


@app.websocket('/chat/ws')
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
