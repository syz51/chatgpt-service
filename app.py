import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware

from translate.api import router as translate_router
from chat import service as chat_service
from chat.model import ChatRequest, ChatResponse, MessagesRequest, ConversationsRequest
from config import get_environment
from db.client import GraphQLClient, gql_client


@asynccontextmanager
async def lifespan(application):
    client = gql_client()
    yield
    await client.client.close_async()


app = FastAPI(lifespan=lifespan, openapi_url=None)

origins = [
    get_environment().allowed_origin,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(translate_router)


@app.get('/')
async def hello():
    return {'Hello': 'World'}


@app.post('/messages')
async def messages(request: MessagesRequest, client: GraphQLClient = Depends(gql_client)):
    return await client.get_messages(request.user_id, request.conversation_id)


@app.post('/conversations')
async def conversations(request: ConversationsRequest, client: GraphQLClient = Depends(gql_client)):
    return await client.list_conversations(request.user_id)


@app.websocket('/chat/ws')
async def chat(websocket: WebSocket, client: GraphQLClient = Depends(gql_client)):
    await websocket.accept()
    while True:
        try:
            request = ChatRequest.parse_obj(await websocket.receive_json())
            await chat_service.chat(request, websocket, client)
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
