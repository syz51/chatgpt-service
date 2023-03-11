import openai

from models import get_settings

openai.api_key = get_settings().openai_api_key


async def chat(messages: list):
    completion = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo",
                                                     messages=messages)
    return completion.choices[0].message.content
