import os
from dotenv import load_dotenv

def load_environment():
    load_dotenv()  # Load environment variables from .env file
    return {
        'app_log_level': os.getenv('LOG_LEVEL', 'ERROR'),
        'libs_log_level': os.getenv('LOG_3RD_PARTY', 'ERROR'),
        'low_log_level': os.getenv('LOW_LOG_LEVEL', 'ERROR'),
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
    }