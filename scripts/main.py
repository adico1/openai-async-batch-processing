"""
Main script to run the batch processor.

This script initializes the environment,
sets up signal handlers for graceful shutdown,
and runs the main batch processing loop.
It uses the OpenAI SDK for monitoring and handling
batch jobs and provides a test function to simulate
batch job processing.

Imports:
    asyncio: Asynchronous I/O
    signal: Signal handling
    load_dotenv: Load environment variables from a .env file
    init_monitoring, EventHandler,
    retrieve_batches_results_handler,
    graceful_shutdown: OpenAI SDK functions

Functions:
    handle_event(event): Handles events by retrieving batch results.
    main(): Main function to run the batch processor.
"""

import asyncio
import env_loader  # pylint: disable=unused-import
from init_server import test_script, run_main

from openai_batch_sdk import (
    init_monitoring,
    EventHandler,
    retrieve_batches_results_handler,
    graceful_shutdown,
    setup_signal_handlers,
)


async def handle_event(event):
    """
    Handles events by retrieving batch results.

    Args:
        event: The event data.

    Actions:
        Retrieves and prints the batch processing result.
    """
    result = await retrieve_batches_results_handler(event)
    print(f"Batch processing result: {result}")


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
        lambda event: asyncio.create_task(handle_event(event)),
    )
    add_batch_job = init_monitoring(event_handler)

    await test_script(add_batch_job, "tests/mock_data.jsonl")


if __name__ == "__main__":
    run_main(main, graceful_shutdown, setup_signal_handlers)
