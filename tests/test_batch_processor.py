import asyncio
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.advanced_batch_processor import init_monitoring
from src.event_handler import EventHandler


class TestBatchProcessor(unittest.TestCase):
    @patch('src.batch_processor.openai.File.create')
    @patch('src.batch_processor.openai.Batch.create')
    @patch('src.batch_processor.openai.Batch.retrieve')
    @patch('src.batch_processor.openai.File.download')
    def test_batch_submission(self, mock_download, mock_retrieve, mock_create_batch, mock_create_file):
        event_handler = EventHandler()
        mock_jsonl_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock_data.jsonl'))

        # Mock the file creation response
        mock_create_file.return_value = {'id': 'file-123'}

        # Mock the batch creation response
        mock_create_batch.return_value = {'id': 'batch-123'}

        # Mock the batch retrieval response to simulate completion
        mock_retrieve.return_value.status = 'completed'
        mock_retrieve.return_value.output_file_id = 'result-file-123'

        # Mock the file download content
        mock_download.return_value.read.return_value = b'{"custom_id": "1", "response": {"body": {"choices": [{"message": {"content": "Ad content"}}]}}}\n'

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(init_monitoring(mock_jsonl_path, event_handler)))

if __name__ == "__main__":
    unittest.main()
