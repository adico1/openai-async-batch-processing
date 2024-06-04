"""
This module loads environment variables from a .env file when imported.
"""

from dotenv import load_dotenv


def load_env():
    """Load environment variables from a .env file."""
    if not load_dotenv(verbose=True):
        print("No .env file found, using environment variables.")
    else:
        print("Loaded environment variables from .env file.")


# Self-execute the load_env function when this module is imported
load_env()
