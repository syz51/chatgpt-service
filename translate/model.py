from pydantic import BaseModel

chinese_sys = 'I want you to act as an Chinese translator and improver. I will speak to you in any language and ' \
              'you will detect the language, translate it and answer in the corrected and improved version of my ' \
              'text, in Chinese. I want you to replace my words and sentences with more beautiful and elegant ' \
              'Chinese words and sentences. Keep the meaning same, but make them more literary. I want you to ' \
              'only reply the correction, the improvements and nothing else, do not write explanations.'

subs_sys = 'I want you to act as a Chinese subtitles translator and improver. I will send you some text from ' \
           '{file_type} file in {language} and you will translate it to Chinese. Dont change the existing formatting.' \
           ' Try to be as fluent and native as possible. Avoid translationese. Do not write explanations, nor any ' \
           'notes. Try to translate even without context. If you really cant translate something at all, or the input' \
           ' doesnt have text to translate, just send [ERROR CANT TRANSLATE] followed by the reason.'


class TranslateRequest(BaseModel):
    message: str
    language: str
    file_type: str
