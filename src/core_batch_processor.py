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
from datetime import datetime

from deps.oai.batch_api.batch_api import (check_batch_status,
                                          retrieve_batch_result,
                                          submit_batch_job)
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

log_pfx = "[📲🤖🎯]"
p_logger = logger.getChild(log_pfx)

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
async def retrieve_batches_results(result_file_id):
  """Retrieves results for completed batch jobs."""
  return retrieve_batch_result(result_file_id)

async def retrieve_batches_results_handler(batch_completed_event):
  """Retrieves results for completed batch jobs."""
  batch_id = batch_completed_event['batch_id']
  result_file_id = batch_completed_event['result_file_id']
  p_logger.info(f"Starting Retrieve Result Process of batch: {batch_id}.")
  return retrieve_batches_results(result_file_id)

# ==============================================================================
# Batch Job Status Check
# ==============================================================================
def stop_processing_status(status):
  stop_processing_statuses = {"cancelled", "cancelling", "expired", "completed", "failed"}
  return status in stop_processing_statuses

def resume_processing_status(status):
  resume_processing_statuses = {"validating", "in_progress", "finalizing"}
  return status in resume_processing_statuses

async def check_batches_results(event_handler, monitored_batch_ids, batch_id):
  """Checks the status of batch jobs and triggers appropriate events."""
  p_logger.info(f"Starting Check Batch Result Process for {batch_id}.")
  response = check_batch_status(batch_id=batch_id)
  p_logger.debug(response)
  if resume_processing_status(response.status):
    p_logger.debug(f"Batch {batch_id} is validating.")
  elif stop_processing_status(response.status):
    del monitored_batch_ids[str(batch_id)]
    event_handler.trigger_event("batch_processing_completed", {
      'status': 'response_ready',
      'batch_id': batch_id,
      'response': response,
    })
# ==============================================================================
# Batch Job Monitoring
# ==============================================================================
async def monitor_batches(event_handler, monitored_batch_ids, aborted):
  """Monitors batch jobs and checks their results periodically."""
  while not aborted.is_set():
    p_logger.debug("Checking batch results...")
    if monitored_batch_ids:
      p_logger.debug("Checking monitored batch results...")
      for batch_id in list(monitored_batch_ids.keys()):
        try:
          await check_batches_results(event_handler, monitored_batch_ids, batch_id)
        except Exception as e:
          p_logger.error(f"Error checking batch results: {e}")
    await asyncio.sleep(30)
  p_logger.debug("Monitor shutdown.")

def init_monitoring(event_handler):
  """Initializes batch job monitoring."""
  monitored_batch_ids = {}
  asyncio.create_task(monitor_batches(event_handler, monitored_batch_ids, aborted))

  return gen_submit_batch_job(monitored_batch_ids)

def graceful_shutdown():
  """Signals the monitoring to stop gracefully."""
  aborted.set()
