from fastapi import APIRouter
from langchain import LLMChain
from langchain.callbacks import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI

from config import get_environment
from translate.model import TranslateRequest, prompt

router = APIRouter(prefix='/translate')


@router.post("/chinese")
async def translate_to_chinese(req: TranslateRequest):
    env = get_environment()

    model = ChatOpenAI(openai_api_key=env.openai_api_key, model_kwargs={'temperature': 0},
                       max_retries=1, callback_manager=AsyncCallbackManager(handlers=[]))
    chain = LLMChain(prompt=prompt, llm=model, callback_manager=AsyncCallbackManager(handlers=[]))
    return await chain.apredict(text=req.message)
