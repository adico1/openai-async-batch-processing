"""
This module provides functionality to create a mock JSONL file
containing example conversations for testing purposes.
"""

from utils.jsonl_handler import create_json_line, write_jsonl_file
from utils.gpt_conversation_handler import Role, create_message
from utils.project import get_project_root


def create_mock_file():
    """
    Creates a mock JSONL file with example conversations between
    a marketing assistant AI and a user.

    The generated file includes conversations highlighting product benefits,
    special offers, and call-to-action prompts to drive affiliate sales.
    """

    # Example usage for multiple conversations
    system_message = create_message(
        Role.SYSTEM,
        (
            "You are a marketing assistant specializing in writing"
            "engaging and persuasive ads for a Telegram store channel."
            "Focus on creating content that highlights product benefits,"
            "special offers, and call-to-action prompts to drive"
            "affiliate sales, additionally add hashtags and keywords"
            "to increase the reach of your ads."
        ),
    )
    user_message = create_message(
        Role.USER, "Can you write an ad for our new product launch?"
    )
    assistant_message = create_message(
        Role.ASSISTANT,
        (
            "Sure! Here is a draft for the ad: "
            "'Introducing our latest product!"
            "Get 20% off for a limited time."
            "#NewProduct #Sale #TelegramStore'",
        ),
    )

    conversation_1 = [system_message, user_message, assistant_message]

    json_line = create_json_line(custom_id=1, conversation=conversation_1)
    print(json_line)
    user_message_2 = create_message(Role.USER, "Write an ad for our summer sale.")
    conversation_1 = [system_message, user_message, assistant_message]
    conversation_2 = [system_message, user_message_2]

    json_line_1 = create_json_line(
        custom_id="conversation_1", conversation=conversation_1
    )
    json_line_2 = create_json_line(
        custom_id="conversation_2", conversation=conversation_2
    )

    write_jsonl_file(
        f"{get_project_root()}/tests/mock_data.jsonl", [json_line_1, json_line_2]
    )
