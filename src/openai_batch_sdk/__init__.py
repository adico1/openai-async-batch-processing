"""
Module: openai_batch_sdk

Description:
This module serves as the main entry point for the OpenAI batch SDK.
It sets up logging and provides access to core functionalities
such as initializing batch job monitoring,
handling batch results retrieval, and managing graceful shutdowns.
It also includes the event handler for managing events related to batch processing.

Public Exports:
  - init_monitoring: Initializes batch job monitoring.
  - graceful_shutdown: Signals the monitoring to stop gracefully.
  - retrieve_batches_results_handler: Handles the retrieval of batch job results.
  - retrieve_batches_results: Retrieves results for completed batch jobs.
  - EventHandler: Manages events for batch job processing.

Setup:
- The module configures logging using the setup_logging function.
"""

from utils.logging import setup_logging
from .core import (
    init_monitoring,
    graceful_shutdown,
    retrieve_batches_results_handler,
    retrieve_batches_results,
    setup_signal_handlers,
)
from .advanced import (
    init_monitoring_l2,
    graceful_shutdown_l2,
    retrieve_batches_results_handler_l2,
    retrieve_batches_results_v2,
    setup_signal_handlers_l2,
)
from .event_handler import EventHandler

__all__ = [
    "init_monitoring",
    "EventHandler",
    "graceful_shutdown",
    "retrieve_batches_results_handler",
    "retrieve_batches_results",
    "setup_signal_handlers",
    "init_monitoring_l2",
    "graceful_shutdown_l2",
    "retrieve_batches_results_handler_l2",
    "retrieve_batches_results_v2",
    "setup_signal_handlers_l2",
]

setup_logging()
