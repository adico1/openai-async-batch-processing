"""
Common utility functions for batch processing scripts.
"""

import asyncio
import signal
import sys


async def test_script(add_batch_job, mock_jsonl_path):
    """
    Script to test batch processing functionality.

    Args:
        add_batch_job (function): Function to add a batch job for the given file path.
        mock_jsonl_path (str): Path to the mock JSONL file.
    """
    print("Starting batch processor...")

    print("Adding batch job...")

    try:
        batch_id = add_batch_job(mock_jsonl_path)
        print(f"Batch job added with ID: {batch_id}")
    except Exception as ex:
        print(f"Error adding batch job: {ex}")
        sys.exit(1)

    # Keep the application running for testing purposes
    await asyncio.sleep(3600)


def run_main(main_func, graceful_shutdown_func, signal_setup_func):
    """
    Runs the main event loop with proper signal handling.

    Args:
        main_func (function): The main coroutine to run.
        graceful_shutdown_func (function): Function to handle graceful shutdown.
        signal_setup_func (function): Function to setup signal handlers.
    """
    loop = asyncio.get_event_loop()
    signal_setup_func(loop)
    try:
        loop.run_until_complete(main_func())
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down...")
        loop.run_until_complete(graceful_shutdown_func(signal.SIGINT, loop))
    finally:
        print("Cleaning up tasks...")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Event loop closed.")
