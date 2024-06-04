"""
Module: conversation_utils

Description:
This module provides utilities for handling and creating
conversation messages in the context of GPT-based applications.
It includes definitions for message roles, a dataclass for
encapsulating message details, and functions for creating
messages and conversations.

Classes:
  - Role: Enum representing the role of a message in a conversation.
  - GPTMessage: Dataclass representing a message in a conversation.

Functions:
  - create_message: Creates a GPTMessage object.
  - create_conversation: Creates a list of dictionaries
  representing a conversation from a list of GPTMessage objects.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class Role(Enum):
    """
    Enum representing the role of a message in a conversation.
    """

    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


@dataclass
class GPTMessage:
    """
    Dataclass representing a message in a conversation.

    Attributes:
        role (Role): The role of the message (user, system, assistant).
        content (str): The content of the message.
    """

    role: Role
    content: str


def create_message(role: Union[Role, str], content: str) -> GPTMessage:
    """
    Create a GPTMessage object.

    Args:
        role (Union[Role, str]): The role of the message.
        Can be a Role enum or a string.
        content (str): The content of the message.

    Returns:
        GPTMessage: The created GPTMessage object.
    """
    if isinstance(role, str):
        role = Role(role)
    return GPTMessage(role=role, content=content)


def create_conversation(messages: List[GPTMessage]) -> List[dict]:
    """
    Create a list of dictionaries representing a
    conversation from a list of GPTMessage objects.

    Args:
        messages (List[GPTMessage]): A list of GPTMessage objects.

    Returns:
        List[dict]: A list of dictionaries representing the conversation.
    """
    return [
        {"role": message.role.value, "content": message.content} for message in messages
    ]
