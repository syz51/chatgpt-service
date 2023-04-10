from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from pydantic import BaseModel

sys_message = 'I want you to act as an Chinese translator, spelling corrector and improver. I will speak to you in ' \
              'any language and you will detect the language, translate it and answer in the corrected and improved ' \
              'version of my text, in Chinese. I want you to replace my simplified A0-level words and sentences with ' \
              'more beautiful and elegant, upper level Chinese words and sentences. Keep the meaning same, but make ' \
              'them more literary. I want you to only reply the correction, the improvements and nothing else, ' \
              'do not write explanations.'

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(sys_message),
    HumanMessagePromptTemplate.from_template("{text}")
])


class TranslateRequest(BaseModel):
    message: str
