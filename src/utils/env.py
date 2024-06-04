"""
Module: environment_loader

Description:
This module provides functionality to load environment variables
from a .env file using the python-dotenv package.
It retrieves specific environment variables related to
logging levels and API keys and returns them in a dictionary.

Functions:
  - load_environment: Loads environment variables from
  a .env file and returns them in a dictionary.
"""

import os
from dotenv import load_dotenv


def load_environment():
    """
    Loads environment variables from a .env file.

    This function uses the python-dotenv package to
    load environment variables from a .env file located
    in the project's root directory.
    It retrieves specific environment variables related to
    logging levels and the OpenAI API key.

    Returns:
        dict: A dictionary containing the following environment variables:
            - app_log_level (str):
            The log level for the application (default is "ERROR").
            - libs_log_level (str):
            The log level for third-party libraries (default is "ERROR").
            - low_log_level (str): The low log level (default is "ERROR").
            - openai_api_key (str): The API key for OpenAI.
    """
    load_dotenv()  # Load environment variables from .env file
    return {
        "app_log_level": os.getenv("LOG_LEVEL", "ERROR"),
        "libs_log_level": os.getenv("LOG_3RD_PARTY", "ERROR"),
        "low_log_level": os.getenv("LOW_LOG_LEVEL", "ERROR"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
    }
