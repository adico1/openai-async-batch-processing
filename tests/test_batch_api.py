# tests/test_batch_api.py
import unittest
from unittest.mock import patch, AsyncMock, MagicMock, mock_open
from deps.oai.batch_api.batch_api import upload_batch_file, submit_batch_job, retrieve_batch_result, check_batch_status

class TestBatchAPI(unittest.TestCase):

    @patch('deps.oai.batch_api.batch_api.OpenAI')
    @patch('builtins.open', new_callable=mock_open, read_data='data')
    def test_upload_batch_file(self, mock_file, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.id = "file-id"
        mock_client.files.create.return_value = mock_response

        file_path = "tests/mock_data.jsonl"
        result = upload_batch_file(file_path)

        mock_client.files.create.assert_called_once_with(file=mock_file.return_value, purpose="batch")
        self.assertEqual(result, "file-id")

    @patch('deps.oai.batch_api.batch_api.OpenAI')
    @patch('builtins.open', new_callable=mock_open, read_data='data')
    def test_submit_batch_job(self, mock_file, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_upload_response = MagicMock()
        mock_upload_response.id = "file-id"
        mock_client.files.create.return_value = mock_upload_response

        mock_batch_response = MagicMock()
        mock_batch_response.id = "batch-id"
        mock_client.batches.create.return_value = mock_batch_response

        file_path = "mock_data.jsonl"
        description = "Test description"
        result = submit_batch_job(file_path, description)

        self.assertEqual(result, "batch-id")
        mock_client.batches.create.assert_called_once_with(
            input_file_id="file-id",
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
                "description": description
            }
        )

    @patch('deps.oai.batch_api.batch_api.OpenAI')
    def test_retrieve_batch_result(self, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_client.files.content.return_value = mock_response

        file_id = "file-id"
        result = retrieve_batch_result(file_id)

        mock_client.files.content.assert_called_once_with(file_id)
        self.assertEqual(result, mock_response)

    @patch('deps.oai.batch_api.batch_api.OpenAI')
    def test_check_batch_status(self, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_client.batches.retrieve.return_value = mock_response

        batch_id = "batch-id"
        result = check_batch_status(batch_id)

        mock_client.batches.retrieve.assert_called_once_with(batch_id=batch_id)
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()
