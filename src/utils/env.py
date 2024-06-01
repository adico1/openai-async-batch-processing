import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()  # Load environment variables from .env file
    return {
        'app_log_level': os.getenv('LOG_LEVEL', 'WANRING'),
        'libs_log_level': os.getenv('LOG_3RD_PARTY', 'TRACE'),
        'low_log_level': os.getenv('LOW_LOG_LEVEL', 'WARNING'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
    }