from fastapi import FastAPI

# from service import client
# from service.models import ChatRequest

app = FastAPI()


@app.get('/')
async def hello():
    return {'Hello': 'World'}


# @app.post('/chat')
# async def chat(request: ChatRequest):
#     res = await client.chat(request.messages)
#     return {'result': res}
