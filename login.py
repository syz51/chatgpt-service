from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.post('/login')
async def login():
    return {'Hello': 'World'}


handler = Mangum(app, lifespan="off")
