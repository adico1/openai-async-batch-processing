"""
This module handles the submission, monitoring, and retrieval of batch jobs
using the OpenAI API. It includes functions for logging, batch job submission,
status checking, and result retrieval.

Public Exports:
    - init_monitoring: Initializes batch job monitoring, returns add_batch_job.
    - submit_batch_jobs: Submits batch jobs for processing.
    - add_batch_job: Adds a batch job for the given file path.
    - retrieve_batches_results: Retrieves results for completed batch jobs.
"""

import asyncio
import env_loader  # pylint: disable=unused-import
from init_server import test_script, run_main

from openai_batch_sdk import (
    graceful_shutdown_l2,
    init_monitoring_l2,
    retrieve_batches_results_handler_l2,
    setup_signal_handlers_l2,
    EventHandler,
)


# ==============================================================================
# Main Function
# ==============================================================================
async def handle_event(event, event_handler):
    """
    Handles events by retrieving batch results.

    Args:
        event: The event data.
        event_handler: The event handler instance.

    Actions:
        Retrieves and prints the batch processing result.
    """
    result = await retrieve_batches_results_handler_l2(event, event_handler)
    print(f"Batch processing result: {result}")


# ==============================================================================
# Main Function
# ==============================================================================
async def main():
    """
    Main function to run the batch processor.

    Actions:
        Initializes the event handler, registers events, sets up batch job monitoring,
        and runs the test script.
    """
    event_handler = EventHandler()
    event_handler.register_event(
        "batch_processing_completed",
        lambda event: asyncio.create_task(handle_event(event, event_handler)),
    )
    add_batch_job = init_monitoring_l2(event_handler)

    await test_script(add_batch_job, "tests/mock_data.jsonl")


if __name__ == "__main__":
    run_main(main, graceful_shutdown_l2, setup_signal_handlers_l2)
