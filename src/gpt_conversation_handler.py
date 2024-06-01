from dataclasses import dataclass
from enum import Enum
from typing import List, Union
import json

class Role(Enum):
  USER = "user"
  SYSTEM = "system"
  ASSISTANT = "assistant"

@dataclass
class GPTMessage:
  role: Role
  content: str

def create_message(role: Union[Role, str], content: str) -> GPTMessage:
  if isinstance(role, str):
    role = Role(role)
  return GPTMessage(role=role, content=content)

def create_conversation(messages: List[GPTMessage]) -> List[dict]:
  return [{"role": message.role.value, "content": message.content} for message in messages]
