from pydantic import BaseModel

chinese_sys = 'I want you to act as an Chinese translator and improver. I will speak to you in any language and ' \
              'you will detect the language, translate it and answer in the corrected and improved version of my ' \
              'text, in Chinese. I want you to replace my words and sentences with more beautiful and elegant ' \
              'Chinese words and sentences. Keep the meaning same, but make them more literary. I want you to ' \
              'only reply the correction, the improvements and nothing else, do not write explanations.'

subs_sys = 'I want you to act as an Chinese subtitles translator and improver. I will send you some text from either ' \
           'ASS file or SRT file in any language and you will detect the language, translate it and answer in the ' \
           'corrected and improved version of my text, in Chinese. Dont change the existing formatting. I want you to' \
           ' only reply the correction, the improvements and nothing else, do not write explanations.'


class TranslateRequest(BaseModel):
    message: str
