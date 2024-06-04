"""
Module: batch_processor
Description: This module handles the submission,
monitoring, and retrieval of batch jobs using the OpenAI API.
It includes functions for logging, batch job submission,
status checking, and result retrieval.
Public Exports:
  - init_monitoring: Initializes batch job monitoring, returns add_batch_job.
  - submit_batch_jobs: Submits batch jobs for processing.
  - add_batch_job: Adds a batch job for the given file path.
  - retrieve_batches_results: Retrieves results for completed batch jobs.
"""

import asyncio
import signal
from openai import APIConnectionError, RateLimitError, APIStatusError
from deps.oai.batch_api.batch_api import (
    check_batch_status,
    retrieve_batch_result,
    submit_batch_job,
)
from utils.env import load_environment
from utils.logging import logger

# Global aborted flag
aborted = asyncio.Event()

# ==============================================================================
# Environment Setup
# ==============================================================================
env = load_environment()
# ==============================================================================
# Logging Functions
# ==============================================================================

LOG_PFX = "[📲🤖🎯]"
p_logger = logger.getChild(LOG_PFX)


# ==============================================================================
# Batch Job Submission
# ==============================================================================
def gen_submit_batch_job(monitored_batch_ids, description="batch prompts job"):
    """
    Generates a function to submit batch jobs.

    Args:
        monitored_batch_ids (dict): Dictionary to keep track of monitored batch IDs.
        description (str): Description for the batch prompts job.

    Returns:
        function: A function to add batch jobs given a file path.
    """

    def add_batch_job(file_path):
        """
        Adds a batch job for the given file path.

        Args:
            file_path (str): The path to the file to be uploaded.

        Returns:
            str: The ID of the submitted batch job.
        """
        p_logger.debug(f"Submitting batch job for file: {file_path}")
        batch_id = submit_batch_job(file_path, description)
        monitored_batch_ids[str(batch_id)] = {
            "batch_id": batch_id,
        }
        return batch_id

    return add_batch_job


# ==============================================================================
# Batch Job Retrieval
# ==============================================================================
async def retrieve_batches_results(result_file_id):
    """
    Retrieves results for completed batch jobs.

    Args:
        result_file_id (str): The ID of the result file.

    Returns:
        bytes: The content of the result file.
    """
    return retrieve_batch_result(result_file_id)


async def retrieve_batches_results_handler(batch_completed_event):
    """
    Retrieves results for completed batch jobs.

    Args:
        batch_completed_event (dict): Event containing batch completion information.

    Returns:
        dict: The response containing batch results.
    """
    batch_id = batch_completed_event["batch_id"]
    p_logger.debug(f"Starting Retrieve Result Process of batch: {batch_id}.")
    return batch_completed_event["response"]


# ==============================================================================
# Batch Job Status Check
# ==============================================================================
def stop_processing_status(status):
    """
    Determines if the processing should stop based on the status.

    Args:
        status (str): The status of the batch job.

    Returns:
        bool: True if processing should stop, False otherwise.
    """
    stop_processing_statuses = {
        "cancelled",
        "cancelling",
        "expired",
        "completed",
        "failed",
    }
    return status in stop_processing_statuses


def resume_processing_status(status):
    """
    Determines if the processing should resume based on the status.

    Args:
        status (str): The status of the batch job.

    Returns:
        bool: True if processing should resume, False otherwise.
    """
    resume_processing_statuses = {"validating", "in_progress", "finalizing"}
    return status in resume_processing_statuses


async def check_batches_results(event_handler, monitored_batch_ids, batch_id):
    """
    Checks the status of batch jobs and triggers appropriate events.

    Args:
        event_handler: The event handler instance for triggering events.
        monitored_batch_ids (dict): Dictionary to keep track of monitored batch job IDs.
        batch_id (str): The ID of the batch job to check.
    """
    p_logger.info(f"Starting Check Batch Result Process for {batch_id}.")
    response = check_batch_status(batch_id=batch_id)
    p_logger.debug(response)
    if resume_processing_status(response.status):
        p_logger.debug(f"Batch {batch_id} is validating.")
    elif stop_processing_status(response.status):
        del monitored_batch_ids[str(batch_id)]
        event_handler.trigger_event(
            "batch_processing_completed",
            {
                "status": "response_ready",
                "batch_id": batch_id,
                "response": response,
            },
        )


# ==============================================================================
# Batch Job Monitoring
# ==============================================================================
async def monitor_batches(event_handler, monitored_batch_ids, aborted_flag):
    """
    Monitors batch jobs and checks their results periodically.

    Args:
        event_handler: The event handler instance for triggering events.
        monitored_batch_ids (dict): Dictionary to keep track of monitored batch job IDs.
        aborted_flag (asyncio.Event): Event to signal when monitoring should stop.
    """
    while not aborted_flag.is_set():
        p_logger.debug("Checking batch results...")
        if monitored_batch_ids:
            p_logger.debug("Checking monitored batch results...")
            for batch_id in list(monitored_batch_ids.keys()):
                try:
                    await check_batches_results(
                        event_handler, monitored_batch_ids, batch_id
                    )
                except asyncio.TimeoutError as timeout_ex:
                    p_logger.error(
                        f"Timeout error checking batch results: {timeout_ex}"
                    )
                except APIConnectionError as api_conn_ex:
                    p_logger.error(
                        f"API connection error checking batch results: {api_conn_ex}"
                    )
                except RateLimitError as rate_limit_ex:
                    p_logger.error(
                        f"Rate limit error checking batch results: {rate_limit_ex}"
                    )
                except APIStatusError as api_status_ex:
                    p_logger.error(
                        f"API status error checking batch results: {api_status_ex}"
                    )
                except Exception as ex:  # pylint: disable=broad-except
                    p_logger.error(f"Unexpected error checking batch results: {ex}")

        await asyncio.sleep(30)
    p_logger.debug("Monitor shutdown.")


def init_monitoring(event_handler):
    """
    Initializes batch job monitoring.

    Args:
        event_handler: The event handler instance for triggering events.

    Returns:
        function: A function to add batch jobs given a file path.
    """
    monitored_batch_ids = {}
    asyncio.create_task(monitor_batches(event_handler, monitored_batch_ids, aborted))

    return gen_submit_batch_job(monitored_batch_ids)


def shutdown():
    """
    Signals the monitoring to stop gracefully.
    """
    aborted.set()


async def graceful_shutdown(exit_signal, app_loop):
    """
    Handles graceful shutdown on receiving exit signals.

    Args:
        exit_signal: The signal received (SIGINT, SIGTERM).
        app-loop: The event loop.

    Actions:
        Sets the graceful shutdown flag,
        sleeps for 30 seconds to allow for a graceful shutdown,
        cancels outstanding tasks, and stops the event loop.
    """
    print(f"\nReceived exit signal {exit_signal.name}...")
    shutdown()
    print("Sleeping 30 seconds to allow for graceful shutdown...")
    await asyncio.sleep(30)  # Allow some time for graceful shutdown
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    app_loop.stop()
    print("Shutdown complete.")


def setup_signal_handlers(app_loop):
    """
    Sets up signal handlers for SIGINT and SIGTERM.

    Args:
        app_loop: The event loop.
    """
    for sig in (signal.SIGINT, signal.SIGTERM):
        app_loop.add_signal_handler(
            sig, lambda sig=sig: asyncio.create_task(graceful_shutdown(sig, app_loop))
        )
