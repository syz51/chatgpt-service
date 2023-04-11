import base64

from fastapi import APIRouter

from translate.model import TranslateRequest, chinese_sys, subs_sys
from translate.service import create_chain, generate_prompt

router = APIRouter(prefix='/translate')


@router.post("/chinese")
async def translate_to_chinese(req: TranslateRequest):
    return await create_chain(generate_prompt(chinese_sys)).apredict(text=req.message)


@router.post('/subs')
async def translate_subs(req: TranslateRequest):
    message = base64.b64decode(bytes(req.message, 'ascii')).decode('utf-8')
    return await create_chain(generate_prompt(subs_sys)).apredict(text=message, language=req.language,
                                                                  file_type=req.file_type)
