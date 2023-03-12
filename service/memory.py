from functools import cached_property
from typing import Dict, Any

from dyntastic import DoesNotExist
from langchain.memory import ConversationBufferMemory
from langchain.memory.utils import get_prompt_input_key
from pydantic import BaseModel

from service.models import ChatHistory


class DynamodbChatMemory(ConversationBufferMemory, BaseModel):
    chat_id: str

    class Config:
        keep_untouched = (cached_property,)

    @cached_property
    def chat_history(self) -> ChatHistory:
        try:
            return ChatHistory.get(hash_key=self.chat_id, consistent_read=True)
        except DoesNotExist:
            return ChatHistory(chat_id=self.chat_id)

    @property
    def buffer(self) -> Any:
        return self.chat_history.messages

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        self.chat_history.add_user_message(inputs[prompt_input_key])
        self.chat_history.add_ai_message(outputs[output_key])
        self.chat_history.save()

    def clear(self) -> None:
        self.chat_history.clear()
