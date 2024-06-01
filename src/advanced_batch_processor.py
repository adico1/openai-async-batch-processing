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

from deps.oai.batch_api.batch_api import (check_batch_status,
                                          retrieve_batch_result,
                                          retrieve_batches_results,
                                          submit_batch_job)
from event_handler import EventHandler
from gpt_conversation_handler import Role, create_message
from jsonl_handler import create_json_line, write_jsonl_file
from utils.env import load_environment
from utils.logging import logger, setup_logging
from utils.project import get_project_root

from .core_batch_processor import (check_batches_results, gen_submit_batch_job,
                                   init_monitoring,
                                   retrieve_batches_results_handler)

# ==============================================================================
# Environment Setup
# ==============================================================================
env = load_environment()
# ==============================================================================
# Logging Functions
# ==============================================================================

log_pfx = __file__
p_logger = logger.getChild(log_pfx)
# ==============================================================================
# Batch Job Retrieval
# ==============================================================================
async def retrieve_batches_results_v2(result_file_id):
  """Retrieves results for completed batch jobs."""
  return retrieve_batch_result(result_file_id)

async def retrieve_batches_results_handler_l2(batch_completed_event, event_handler):
  """Retrieves results for completed batch jobs."""
  batch_id = batch_completed_event['batch_id']
  if batch_completed_event['status'] == 'response_ready':
    response = batch_completed_event['response']
    result_file_id = response['result_file_id']
    p_logger.info("Starting Retrieve Result Process.")
    result_file = retrieve_batch_result(result_file_id)
    content = result_file.read()
    p_logger.debug('content', content)
    lines = content.decode().splitlines()
    p_logger.debug('lines', lines)
    event_handler.trigger_event("batch_processing_completed", batch_completed_event)
  else:
    completed = batch_completed_event['completed']
    failed = batch_completed_event['failed']
    errors = [f"{error.code}: {error.message}" for error in batch_completed_event['errors']]
    p_logger.error(f"Batch {batch_id} processing status: completed: {completed}, failed: {failed}, errors: {errors}.")
    event_handler.trigger_event("batch_processing_completed", batch_completed_event)



def init_monitoring_l2(app_event_handler):
  """Initializes batch job monitoring."""
  core_event_handler = EventHandler()
  app_event_handler.register_event(
    "batch_processing_completed",
    lambda event: asyncio.create_task(retrieve_batches_results_handler_l2(event, app_event_handler))
  )
  return init_monitoring(core_event_handler)
