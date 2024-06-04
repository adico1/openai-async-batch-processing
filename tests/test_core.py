"""
file: tests/test_core.py
Unit tests for the core functionality of the openai_batch_sdk.

This module includes tests for the following functions:
- gen_submit_batch_job: Generates a function to submit batch jobs.
- retrieve_batches_results_handler: Handles the retrieval of batch results.
- init_monitoring: Initializes batch job monitoring.
- graceful_shutdown: Signals the monitoring to stop gracefully.

Each test verifies the correctness of these core functions,
ensuring they work as expected with the help of mocks
for external dependencies.
"""

import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from openai_batch_sdk.core import (
    gen_submit_batch_job,
    retrieve_batches_results_handler,
    init_monitoring,
    shutdown,
    aborted,
)


class TestCore(unittest.TestCase):
    """
    Test suite for the core functionality of the openai_batch_sdk.
    """

    @patch("openai_batch_sdk.core.submit_batch_job")
    def test_gen_submit_batch_job(self, mock_submit_batch_job):
        """
        Test the gen_submit_batch_job function to ensure it correctly generates
        a function to submit batch jobs.

        Args:
            mock_submit_batch_job: Mock for the submit_batch_job function.

        Asserts:
            The submit_batch_job function is called once with the correct parameters.
            The function returns the expected batch ID.
            The batch ID is added to the monitored batch IDs.
        """
        mock_submit_batch_job.return_value = "batch-id"
        monitored_batch_ids = {}

        add_batch_job = gen_submit_batch_job(monitored_batch_ids, "test description")
        result = add_batch_job("mock_data.jsonl")

        mock_submit_batch_job.assert_called_once_with(
            "mock_data.jsonl", "test description"
        )
        self.assertEqual(result, "batch-id")
        self.assertIn("batch-id", monitored_batch_ids)

    @patch("openai_batch_sdk.core.retrieve_batches_results", new_callable=AsyncMock)
    def test_retrieve_batches_results_handler(self, mock_retrieve_batches_results):
        """
        Test the retrieve_batches_results_handler function to ensure it correctly
        handles the retrieval of batch results.

        Args:
            mock_retrieve_batches_results:
            Mock for the retrieve_batches_results function.

        Asserts:
            The function returns the expected response.
        """
        mock_response = MagicMock()
        mock_retrieve_batches_results.return_value = mock_response

        batch_completed_event = {"batch_id": "batch-id", "response": mock_response}
        result = asyncio.run(retrieve_batches_results_handler(batch_completed_event))

        self.assertEqual(result, mock_response)

    @patch("openai_batch_sdk.core.monitor_batches", new_callable=AsyncMock)
    def test_init_monitoring(self, mock_monitor_batches):
        """
        Test the init_monitoring function to ensure it correctly initializes
        batch job monitoring.

        Args:
            mock_monitor_batches: Mock for the monitor_batches function.

        Asserts:
            The returned add_batch_job function is of the correct type.
            The monitor_batches function is called once.
        """
        event_handler = MagicMock()
        monitored_batch_ids = {}

        async def run_test():
            add_batch_job = init_monitoring(event_handler)
            self.assertIsInstance(
                add_batch_job,
                type(gen_submit_batch_job(monitored_batch_ids, "test description")),
            )
            mock_monitor_batches.assert_called_once()

        asyncio.run(run_test())

    def test_graceful_shutdown(self):
        """
        Test the graceful_shutdown function to ensure it correctly signals
        the monitoring to stop.

        Asserts:
            The aborted event is not set before calling graceful_shutdown.
            The aborted event is set after calling graceful_shutdown.
        """
        # Ensure the aborted event is not set before calling graceful_shutdown
        aborted.clear()
        self.assertFalse(aborted.is_set())

        # Call graceful_shutdown to set the aborted event
        shutdown()

        # Check that the aborted event is set
        self.assertTrue(aborted.is_set())

        # Reset the aborted event after the test
        aborted.clear()


if __name__ == "__main__":
    unittest.main()
