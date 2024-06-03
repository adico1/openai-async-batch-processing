# tests/test_core.py
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
from openai_batch_sdk.core import gen_submit_batch_job, retrieve_batches_results_handler, init_monitoring, graceful_shutdown

class TestCore(unittest.TestCase):

    @patch('openai_batch_sdk.core.submit_batch_job')
    def test_gen_submit_batch_job(self, mock_submit_batch_job):
        mock_submit_batch_job.return_value = "batch-id"
        monitored_batch_ids = {}

        add_batch_job = gen_submit_batch_job(monitored_batch_ids, "test description")
        result = add_batch_job("mock_data.jsonl")

        mock_submit_batch_job.assert_called_once_with("mock_data.jsonl", "test description")
        self.assertEqual(result, "batch-id")
        self.assertIn("batch-id", monitored_batch_ids)

    @patch('openai_batch_sdk.core.retrieve_batches_results', new_callable=AsyncMock)
    def test_retrieve_batches_results_handler(self, mock_retrieve_batches_results):
        mock_response = MagicMock()
        mock_retrieve_batches_results.return_value = mock_response

        batch_completed_event = {'batch_id': 'batch-id', 'response': mock_response}
        result = asyncio.run(retrieve_batches_results_handler(batch_completed_event))

        self.assertEqual(result, mock_response)

    @patch('openai_batch_sdk.core.monitor_batches', new_callable=AsyncMock)
    def test_init_monitoring(self, mock_monitor_batches):
        event_handler = MagicMock()
        monitored_batch_ids = {}

        async def run_test():
            add_batch_job = init_monitoring(event_handler)
            self.assertIsInstance(add_batch_job, type(gen_submit_batch_job(monitored_batch_ids, "test description")))
            mock_monitor_batches.assert_called_once()

        asyncio.run(run_test())

    def test_graceful_shutdown(self):
        graceful_shutdown()
        self.assertTrue(asyncio.Event().is_set())

if __name__ == '__main__':
    unittest.main()
