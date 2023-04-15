import json
from functools import lru_cache
from typing import List
from uuid import UUID

from fastapi import HTTPException
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import parse_obj_as

from chat.model import HumanChatMessage, AIChatMessage
from config import get_environment
from db.requests import query_list_conversations, query_get_messages, create_messages_request_variables, \
    create_conversations_request_variables, mutation_create_conversation_version, \
    mutation_conversation_version_variables, mutation_update_conversation_version, \
    mutation_update_conversation_version_variables


class GraphQLClient:
    def __init__(self):
        env = get_environment()
        transport = AIOHTTPTransport(url=env.db_url, headers={'apikey': env.db_key})
        self.client = Client(transport=transport)

    async def list_conversations(self, user_id: UUID):
        res = await self.client.execute_async(query_list_conversations,
                                              variable_values=await create_conversations_request_variables(user_id))
        conversations = res['conversationsCollection']['edges']
        return [conversation['node'] for conversation in conversations]

    async def get_messages(self, user_id: UUID, conversation_id: UUID):
        res = await self.client.execute_async(query_get_messages,
                                              variable_values=await create_messages_request_variables(user_id,
                                                                                                      conversation_id))
        conversations = res['conversationsCollection']['edges']
        if len(conversations) == 0:
            raise HTTPException(status_code=404, detail=f'Error accessing conversation: {conversation_id}')
        messages = conversations[0]['node']['conversation_versionsCollection']['edges']
        if len(messages) == 0:
            return messages
        return parse_obj_as(List[AIChatMessage | HumanChatMessage], json.loads(messages[0]['node']['messages']))

    async def create_conversation_version(self, conversation_id: UUID, messages: List):
        await self.client.execute_async(mutation_create_conversation_version,
                                        variable_values=await mutation_conversation_version_variables(
                                            conversation_id, messages))

    async def update_conversation_version(self, conversation_id: UUID, messages: List):
        await self.client.execute_async(mutation_update_conversation_version,
                                        variable_values=await mutation_update_conversation_version_variables(
                                            conversation_id, messages))


@lru_cache(maxsize=1)
def gql_client() -> GraphQLClient:
    return GraphQLClient()
