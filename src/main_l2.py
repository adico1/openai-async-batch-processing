# ==============================================================================
# File: batch_processor.py
# Description: This module handles the submission, monitoring, and retrieval of batch jobs using the OpenAI API. It includes functions for logging, batch job submission, status checking, and result retrieval.
# Public Exports:
#   - init_monitoring: Initializes batch job monitoring, returns add_batch_job.
#   - submit_batch_jobs: Submits batch jobs for processing.
#   - add_batch_job: Adds a batch job for the given file path.
#   - retrieve_batches_results: Retrieves results for completed batch jobs.
# ==============================================================================

import signal
import sys
from concurrent.futures import ThreadPoolExecutor

import asyncio
import time
from datetime import datetime

from deps.oai.batch_api.batch_api import (check_batch_status,
                                             retrieve_batch_result,
                                             submit_batch_job)
from event_handler import EventHandler
from utils.env import load_environment
from utils.logging import logger, setup_logging
from utils.project import get_project_root

from jsonl_handler import create_json_line, write_jsonl_file
from gpt_conversation_handler import Role, create_message


async def shutdown(signal, loop, executor):
    print(f"\nReceived exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Awaiting ThreadPoolExecutor shutdown...")
    executor.shutdown(wait=True)
    print("Shutdown complete.")


def setup_signal_handlers(loop, executor):
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(sig, loop, executor)))


# ==============================================================================
# Environment Setup
# ==============================================================================
env = load_environment()
# ==============================================================================
# Logging Functions
# ==============================================================================
setup_logging()

log_pfx = "[📲🤖🎯]"
p_logger = logger.getChild(log_pfx)

def log_log_start():
  """Logs the start time of the batch processing."""
  p_logger.info(f"[📆📢] started at: {datetime.now().strftime('%Y-%m-%d')}")
  p_logger.debug("🐞 mode on")

log_log_start()

def createMockFile():
  # Example usage for multiple conversations
  # Example Usage
  system_message = create_message(Role.SYSTEM, "You are a marketing assistant specializing in writing engaging and persuasive ads for a Telegram store channel. Focus on creating content that highlights product benefits, special offers, and call-to-action prompts to drive affiliate sales, additionally add hashtags and keywords to increase the reach of your ads.")
  user_message = create_message(Role.USER, "Can you write an ad for our new product launch?")
  assistant_message = create_message(Role.ASSISTANT, "Sure! Here is a draft for the ad: 'Introducing our latest product! Get 20% off for a limited time. #NewProduct #Sale #TelegramStore'")

  conversation_1 = [system_message, user_message, assistant_message]

  json_line = create_json_line(custom_id=1, conversation=conversation_1)
  print(json_line)
  user_message_2 = create_message(Role.USER, "Write an ad for our summer sale.")
  conversation_1 = [system_message, user_message, assistant_message]
  conversation_2 = [system_message, user_message_2]

  json_line_1 = create_json_line(
    custom_id="conversation_1",
    conversation=conversation_1
  )
  json_line_2 = create_json_line(
    custom_id="conversation_2",
    conversation=conversation_2
  )

  write_jsonl_file(f"{get_project_root()}/tests/mock_data.jsonl", [json_line_1, json_line_2])
# ==============================================================================
# Testing Functions
# ==============================================================================
def test_script(add_batch_job):
  """Script to test batch processing functionality."""
  p_logger.debug("Starting batch processor...")

  # Path to the mock JSONL file
  createMockFile()
  mock_jsonl_path = f"{get_project_root()}/tests/mock_data.jsonl"

  p_logger.debug("Adding batch job...")

  try:
    batch_id = add_batch_job(mock_jsonl_path)
    p_logger.debug(f"Batch job added with ID: {batch_id}")
  except Exception as e:
    p_logger.error(f"Error adding batch job: {e}")
    exit(1)

  # Keep the application running for testing purposes
  time.sleep(3600)
# ==============================================================================
# Main Function
# ==============================================================================
async def main():
    """Main function to run the batch processor."""
    event_handler = EventHandler()

    add_batch_job = init_monitoring(event_handler)

    # Run the test script in a separate thread to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, test_script, add_batch_job)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()
    setup_signal_handlers(loop, executor)
    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down...")
        loop.run_until_complete(shutdown(signal.SIGINT, loop, executor))
    finally:
        print("Cleaning up tasks...")
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Event loop closed.")
