"""
Module: logging_setup

Description:
This module sets up custom logging for the application,
including configuring log levels, log formats, and handlers
for console and file logging. It introduces emoji-based
log levels for better visual distinction and allows for
specific feature-based logging filters.

Functions:
  - setup_logging: Configures logging settings for the application.
  - get_lib_logger: Returns a logger for a specific library.
  - get_module_logger: Returns a logger for a specific module.
  - get_ad_processing_logger: Returns a logger for ad processing
  with a specific stage emoji.

Classes:
  - FeatureFilter: A logging filter class for specific feature-based logging.
"""

import logging
import os
import sys
from utils.env import load_environment
from utils.project import get_project_root

env_vars = load_environment()

# Environment variable to set the log level for your application
app_log_level = env_vars["app_log_level"].upper()
libs_log_level = env_vars["libs_log_level"].upper()
low_log_level = env_vars["low_log_level"].upper()

print(f"App log level: {app_log_level}")
print(f"Libs log level: {libs_log_level}")
print(f"Low log level: {low_log_level}")

# Emoji mappings for log levels
log_level_emojis = {
    "DEBUG": "🐞",  # Bug emoji for debug
    "INFO": "📢",  # Information
    "WARNING": "👀",  # Warning sign
    "ERROR": "❗",  # Exclamation mark
    "CRITICAL": "💥",  # Police light for critical issues
}
# Optionally map logger names to emojis (preset for known loggers for performance)
logger_name_emojis = {
    "APP": "🌐",  # Tools for 'myapp'
    "DB": "🗄️",  # Floppy disk for 'database' operations
}

old_factory = logging.getLogRecordFactory()


def emoji_record_factory(*args, **kwargs):
    """
    A custom log record factory that adds emojis to log levels and logger names.

    Args:
        *args: Positional arguments passed to the original log record factory.
        **kwargs: Keyword arguments passed to the original log record factory.

    Returns:
        logging.LogRecord: A log record with modified levelname and name.
    """
    record = old_factory(*args, **kwargs)

    child = record.name.removeprefix("APP.")
    if not child == "APP":
        record.child = f"{child}"
    else:
        record.child = ""

    # Apply pre-defined emoji from mapping, using the existing levelname and name
    record.levelname = log_level_emojis.get(record.levelname.strip(), record.levelname)
    record.name = logger_name_emojis.get("APP", record.name)

    return record


def record_factory(*args, **kwargs):
    """
    A custom log record factory that centers the levelname.

    Args:
        *args: Positional arguments passed to the original log record factory.
        **kwargs: Keyword arguments passed to the original log record factory.

    Returns:
        logging.LogRecord: A log record with centered levelname.
    """
    record = old_factory(*args, **kwargs)
    record.levelname = record.levelname.center(7, " ")
    return record


logging.setLogRecordFactory(emoji_record_factory)

# Basic configuration of logging
# Set the basic configuration for the root logger
logging.basicConfig(level=libs_log_level, handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("APP")
logger.propagate = False
logger.setLevel(app_log_level)


# Custom logger setup
def setup_logging():
    """
    Configures logging settings for the application.

    This function sets up console and file handlers with specified formats,
    applies logging level configurations, and optionally filters logs based on features.
    """
    # Create formatters and add to handlers
    log_format = "%(asctime)s[%(name)s%(levelname)s]%(child)s%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(app_log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (for more persistent logging)
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel("INFO")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optionally, suppress excessive logging from third-party libraries
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)

    # Filter for specific features
    class FeatureFilter(logging.Filter):  # pylint: disable=too-few-public-methods
        """
        A logging filter class for specific feature-based logging.

        This filter allows logs to be enabled for specific features by matching
        the feature name within the log message.

        Attributes:
            feature_name (str): The name of the feature to filter logs for.
        """

        def __init__(self, feature_name):
            super().__init__()
            self.feature_name = feature_name

        def filter(self, record):
            return self.feature_name in record.msg

    # Example: Enabling logs for ad generation feature
    if "FEATURE" in os.getenv("LOG_FEATURES", ""):
        feature_processing_filter = FeatureFilter("FEATURE")
        console_handler.addFilter(feature_processing_filter)
        file_handler.addFilter(feature_processing_filter)


def get_lib_logger(lib_name):
    """
    Returns a logger for a specific library.

    Args:
        lib_name (str): The name of the library.

    Returns:
        logging.Logger: A logger instance for the specified library.
    """
    prj_root_len = len(f"{get_project_root()}/src/")
    log_pfx = f"[{lib_name[prj_root_len:]}]"
    p_logger = logger.getChild(log_pfx)
    p_logger.setLevel(low_log_level)
    return p_logger


def get_module_logger(module_name):
    """
    Returns a logger for a specific module.

    Args:
        module_name (str): The name of the module.

    Returns:
        logging.Logger: A logger instance for the specified module.
    """
    return logger.getChild(module_name)


def get_ad_processing_logger(stage_emoji):
    """
    Returns a logger for ad processing with a specific stage emoji.

    Args:
        stage_emoji (str): The emoji representing the stage of ad processing.

    Returns:
        logging.Logger: A logger instance for app with the specified stage emoji.
    """
    log_pfx = f"[📲🤖{stage_emoji}]"
    p_logger = logger.getChild(log_pfx)
    p_logger.setLevel(app_log_level)
    return p_logger


if __name__ == "__main__":
    setup_logging()
