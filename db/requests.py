import json
from typing import List
from uuid import UUID

from gql import gql
from pydantic.json import pydantic_encoder

query_list_conversations = gql(
    """
query Node(
  $conversationsCollectionOrderBy: [conversationsOrderBy!]
  $filter: conversationsFilter
) {
  conversationsCollection(
    orderBy: $conversationsCollectionOrderBy
    filter: $filter
  ) {
    edges {
      node {
        conversation_id
        title
      }
    }
  }
}
"""
)


async def create_conversations_request_variables(user_id: UUID):
    return {
        "conversationsCollectionOrderBy": [
            {
                "created_at": "DescNullsFirst"
            }
        ],
        "filter": {
            "deleted_at": {
                "is": "NULL"
            },
            "user_id": {
                "eq": str(user_id)
            }
        }
    }


query_get_messages = gql(
    """
query ConversationsCollection($filter: conversationsFilter, $orderBy: [conversation_versionsOrderBy!], $first: Int) {
  conversationsCollection(filter: $filter) {
    edges {
      node {
        conversation_versionsCollection(orderBy: $orderBy, first: $first) {
          edges {
            node {
              messages
            }
          }
        }
      }
    }
  }
}
"""
)


async def create_messages_request_variables(user_id: UUID, conversation_id: UUID):
    return {
        "filter": {
            "user_id": {
                "eq": str(user_id)
            },
            "deleted_at": {
                "is": "NULL"
            },
            "conversation_id": {
                "eq": str(conversation_id)
            }
        },
        "orderBy": [
            {
                "version": "DescNullsFirst"
            }
        ],
        "first": 1
    }


mutation_create_conversation_version = gql(
    """
mutation Mutation($objects: [conversation_versionsInsertInput!]!) {
  insertIntoconversation_versionsCollection(objects: $objects) {
    affectedCount
  }
}
    """
)


async def mutation_conversation_version_variables(conversation_id: UUID, messages: List):
    return {
        "objects": [
            {
                "messages": json.dumps(messages, default=pydantic_encoder),
                "version": 1,
                "conversation_id": str(conversation_id)
            }
        ]
    }
