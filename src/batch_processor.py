# ==============================================================================
# File: batch_processor.py
# Description: This module handles the submission, monitoring, and retrieval of batch jobs using the OpenAI API. It includes functions for logging, batch job submission, status checking, and result retrieval.
# Public Exports:
#   - init_monitoring: Initializes batch job monitoring, returns add_batch_job.
#   - submit_batch_jobs: Submits batch jobs for processing.
#   - add_batch_job: Adds a batch job for the given file path.
#   - retrieve_batches_results: Retrieves results for completed batch jobs.
# ==============================================================================

import asyncio
import time
from datetime import datetime
from threading import Thread

from deps.openai.batch_api.batch_api import (check_batch_status,
                                             retrieve_batch_result,
                                             submit_batch_job)
from event_handler import EventHandler
from utils.env import load_environment
from utils.logging import logger, setup_logging
from utils.project import get_project_root

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
# ==============================================================================
# Batch Job Submission
# ==============================================================================
def gen_submit_batch_job(monitored_batch_ids, description="batch prompts job"):
    """Generates a function to submit batch jobs."""
    def add_batch_job(file_path):
      """Adds a batch job for the given file path."""
      p_logger.debug(f"Submitting batch job for file: {file_path}")
      batch_id = submit_batch_job(file_path, description)
      monitored_batch_ids[str(batch_id)] = {
          'batch_id': batch_id,
      }
      return batch_id

    return add_batch_job
# ==============================================================================
# Batch Job Retrieval
# ==============================================================================
def retrieve_batch_results_handler(batch_completed_event):
    """Retrieves results for completed batch jobs."""
    asyncio.run_coroutine_threadsafe(
      retrieve_batches_results(batch_completed_event),
      asyncio.get_event_loop()
    )

async def retrieve_batches_results(batch_completed_event):
  """Retrieves results for completed batch jobs."""
  batch_id = batch_completed_event['batch_id']
  if batch_completed_event['status'] == 'completed':
    result_file_id = batch_completed_event['result_file_id']
    p_logger.info("Starting Retrieve Result Process.")
    result_file = retrieve_batch_result(result_file_id)
    content = result_file.read()
    p_logger.debug('content', content)
    lines = content.decode().splitlines()
    p_logger.debug('lines', lines)
    return [lines, None]
  else:
    request_counts = batch_completed_event['request_counts']
    completed = request_counts['completed']
    failed = request_counts['failed']
    p_logger.error(f"Batch {batch_id} processing status: completed: {completed}, failed: {failed}.")
    errors = []
    for error in batch_completed_event['errors']:
      errors.append(error)
    return [None, errors]

# ==============================================================================
# Batch Job Status Check
# ==============================================================================
def check_batches_results(event_handler, monitored_batch_ids, batch_id):
  """Checks the status of batch jobs and triggers appropriate events."""
  p_logger.info(f"Starting Check Batch Result Process for {batch_id}.")
  response = check_batch_status(batch_id=batch_id)
  p_logger.debug(response)
  if response.status == 'validating':
      p_logger.debug(f"Batch {batch_id} is validating.")
  elif response.status == 'completed':
      result_file_id = response.output_file_id
      event_handler.trigger_event("batch_completed", {
        'status': 'completed',
        'batch_id': batch_id,
        'result_file_id': result_file_id
      })
  elif response.status == 'failed':
      del monitored_batch_ids[str(batch_id)]
      event_handler.trigger_event("batch_completed", {
        'status': 'failed',
        'batch_id': batch_id
      })
# ==============================================================================
# Batch Job Monitoring
# ==============================================================================
def monitor_batches(event_handler, monitored_batch_ids):
  """Monitors batch jobs and checks their results periodically."""
  while True:
    p_logger.debug("Checking batch results...")
    if monitored_batch_ids:
      p_logger.debug("Checking monitored batch results...")
      for batch_id in list(monitored_batch_ids.keys()):
        try:
          check_batches_results(event_handler, monitored_batch_ids, batch_id)
        except Exception as e:
          print(f"Error checking batch results: {e}")

    time.sleep(30)

def init_monitoring(event_handler):
  """Initializes batch job monitoring."""
  monitored_batch_ids = {}
  event_handler.register_event("batch_completed", retrieve_batch_results_handler)
  monitor_thread = Thread(target=monitor_batches, args=(event_handler, monitored_batch_ids), daemon=True)
  monitor_thread.start()

  return gen_submit_batch_job(monitored_batch_ids)

# ==============================================================================
# Testing Functions
# ==============================================================================
def test_script(add_batch_job):
  """Script to test batch processing functionality."""
  print("Starting batch processor...")

  # Path to the mock JSONL file
  mock_jsonl_path = f"{get_project_root()}/tests/mock_data.jsonl"

  p_logger.debug("Adding batch job...")

  try:
    batch_id = add_batch_job(mock_jsonl_path)
    p_logger.debug(f"Batch job added with ID: {batch_id}")
  except Exception as e:
    p_logger.error(f"Error adding batch job: {e}")
    exit(1)

  # Keep the application running
  time.sleep(3600)
# ==============================================================================
# Main Function
# ==============================================================================
async def main():
  """Main function to run the batch processor."""
  event_handler = EventHandler()

  monitor_batch = init_monitoring(event_handler)

  tasks = [
    asyncio.to_thread(test_script, monitor_batch)
  ]
  await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())