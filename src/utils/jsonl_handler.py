"""
Module: jsonl_handler

Description:
This module provides utility functions for creating JSON lines (jsonl)
and writing them to files.
It includes functions to create individual JSON lines from conversations
and write multiple JSON lines to a file.

Functions:
  - create_json_line: Creates a JSON line from a conversation.
  - write_jsonl_file: Writes multiple JSON lines to a file.
"""

import json
from typing import List
from src.utils.gpt_conversation_handler import (
    GPTMessage,
    create_conversation,
)


def create_json_line(
    custom_id: str,
    conversation: List[GPTMessage],
    model: str = "gpt-4",
    max_tokens: int = 1500,
) -> str:
    """
    Creates a JSON line from a conversation.

    Args:
        custom_id (str): The custom ID for the conversation.
        conversation (List[GPTMessage]): The conversation messages.
        model (str): The model to use for the conversation (default is "gpt-4").
        max_tokens (int): The maximum number of tokens for the
        conversation (default is 1500).

    Returns:
        str: A JSON string representing the conversation.
    """
    json_line = {
        "custom_id": custom_id,
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": model,
            "messages": create_conversation(conversation),
            "max_tokens": max_tokens,
        },
    }
    return json.dumps(json_line)


def write_jsonl_file(filename: str, conversations: List[dict]) -> None:
    """
    Writes multiple JSON lines to a file.

    Args:
        filename (str): The name of the file to write to.
        conversations (List[str]): A list of JSON strings representing conversations.

    Returns:
        None
    """
    with open(filename, "w", encoding="utf-8") as file:
        for conversation in conversations:
            file.write(conversation + "\n")
