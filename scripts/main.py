# Description: Main script to run the batch processor.
import asyncio
import signal
from dotenv import load_dotenv

if not load_dotenv(verbose=True):
  print("No .env file found, using environment variables.")
else:
  print("Loaded environment variables from .env file.")

from openai_batch_sdk import init_monitoring, EventHandler, retrieve_batches_results_handler, graceful_shutdown

async def shutdown(signal, loop):
    print(f"\nReceived exit signal {signal.name}...")
    graceful_shutdown()
    print("Sleeping 30 seconds to allow for graceful shutdown...")
    await asyncio.sleep(30)  # Allow some time for graceful shutdown
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")


def setup_signal_handlers(loop):
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(sig, loop)))
# ==============================================================================
# Testing Functions
# ==============================================================================
async def test_script(add_batch_job):
  """Script to test batch processing functionality."""
  print("Starting batch processor...")

  # Path to the mock JSONL file
  mock_jsonl_path = f"mock_data.jsonl"

  print("Adding batch job...")

  try:
    batch_id = add_batch_job(mock_jsonl_path)
    print(f"Batch job added with ID: {batch_id}")
  except Exception as e:
    print(f"Error adding batch job: {e}")
    exit(1)

  # Keep the application running for testing purposes
  await asyncio.sleep(3600)
# ==============================================================================
# Main Function
# ==============================================================================
async def handle_event(event):
    result = await retrieve_batches_results_handler(event)
    print(f"Batch processing result: {result}")

async def main():
  """Main function to run the batch processor."""
  event_handler = EventHandler()
  event_handler.register_event(
    "batch_processing_completed",
    lambda event: asyncio.create_task(handle_event(event))
  )
  add_batch_job = init_monitoring(event_handler)

  await test_script(add_batch_job)

if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  setup_signal_handlers(loop)
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
