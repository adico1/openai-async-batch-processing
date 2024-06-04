"""
Module: batch_processor

Description:
This module handles the submission, monitoring, and retrieval of batch
jobs using the OpenAI API. It includes functions for logging,
batch job submission, status checking, and result retrieval.
The module supports both basic and advanced batch processing workflows.

Public Exports:
  - init_monitoring: Initializes batch job monitoring, returns add_batch_job.
  - retrieve_batches_results_v2: Retrieves results for completed batch jobs.
  - retrieve_batches_results_handler_l2: Handles retrieval of batch results
   and triggers events.
  - init_monitoring_l2: Initializes batch job monitoring with advanced features.
"""

import asyncio

from deps.oai.batch_api.batch_api import retrieve_batch_result
from src.openai_batch_sdk.event_handler import EventHandler
from utils.env import load_environment
from utils.logging import logger

from .core import graceful_shutdown, init_monitoring, setup_signal_handlers

# ==============================================================================
# Environment Setup
# ==============================================================================
env = load_environment()
# ==============================================================================
# Logging Functions
# ==============================================================================

LOG_PFX = __file__
p_logger = logger.getChild(LOG_PFX)


# ==============================================================================
# Batch Job Retrieval
# ==============================================================================
async def retrieve_batches_results_v2(result_file_id):
    """
    Retrieves results for completed batch jobs.

    Args:
        result_file_id (str): The ID of the result file.

    Returns:
        bytes: The content of the result file.
    """
    return retrieve_batch_result(result_file_id)


async def retrieve_batches_results_handler_l2(batch_completed_event, event_handler):
    """
    Handles retrieval of batch results for completed batch jobs
    and triggers appropriate events.

    Args:
        batch_completed_event (dict): Event containing batch completion information.
        event_handler (EventHandler): The event handler instance for triggering events.
    """
    batch_id = batch_completed_event["batch_id"]
    if batch_completed_event["status"] == "response_ready":
        response = batch_completed_event["response"]
        result_file_id = response["result_file_id"]
        p_logger.info("Starting Retrieve Result Process.")
        result_file = retrieve_batch_result(result_file_id)
        content = result_file.read()
        p_logger.debug("content", content)
        lines = content.decode().splitlines()
        p_logger.debug("lines", lines)
        event_handler.trigger_event("batch_processing_completed", batch_completed_event)
    else:
        completed = batch_completed_event["completed"]
        failed = batch_completed_event["failed"]
        errors = [
            f"{error.code}: {error.message}"
            for error in batch_completed_event["errors"]
        ]
        p_logger.error(
            f"Batch {batch_id} processing status: "
            f"completed: {completed}, failed: {failed}, errors: {errors}."
        )
        event_handler.trigger_event("batch_processing_completed", batch_completed_event)


def init_monitoring_l2(app_event_handler):
    """
    Initializes batch job monitoring with advanced features.

    Args:
        app_event_handler (EventHandler): The application-level event handler instance.

    Returns:
        function: A function to add batch jobs given a file path.
    """
    core_event_handler = EventHandler()
    app_event_handler.register_event(
        "batch_processing_completed",
        lambda event: asyncio.create_task(
            retrieve_batches_results_handler_l2(event, app_event_handler)
        ),
    )
    return init_monitoring(core_event_handler)


def graceful_shutdown_l2(exit_signal, app_loop):
    """
    Signals the monitoring to stop gracefully.
    """
    graceful_shutdown(exit_signal, app_loop)


def setup_signal_handlers_l2(app_loop):
    """
    Sets up signal handlers for SIGINT and SIGTERM.

    Args:
        app_loop: The event loop.
    """
    setup_signal_handlers(app_loop)
