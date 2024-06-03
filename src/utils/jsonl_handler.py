from dataclasses import dataclass, asdict
from enum import Enum
import json
from typing import List
from src.utils.gpt_conversation_handler import Role, GPTMessage, create_message, create_conversation

def create_json_line(
  custom_id: str,
  conversation: List[GPTMessage],
  model: str = "gpt-4",
  max_tokens: int = 1500
) -> str:
  json_line = {
    "custom_id": custom_id,
    "method": "POST",
    "url": "/v1/chat/completions",
    "body": {
      "model": model,
      "messages": create_conversation(conversation),
      "max_tokens": max_tokens
    }
  }
  return json.dumps(json_line)

def write_jsonl_file(filename: str, conversations: List[dict]) -> None:
  with open(filename, 'w') as file:
    for conversation in conversations:
      file.write(conversation + '\n')
