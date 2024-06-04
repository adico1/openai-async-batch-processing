"""
file: tests/test_batch_api.py
Unit tests for the core functionality of the openai_batch_sdk module.

This module includes tests for the following functions:
- gen_submit_batch_job
- retrieve_batches_results_handler
- init_monitoring
- graceful_shutdown
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
from deps.oai.batch_api.batch_api import (
    upload_batch_file,
    submit_batch_job,
    retrieve_batch_result,
    check_batch_status,
)


class TestBatchAPI(unittest.TestCase):
    """
    Test suite for the batch API functions.
    """

    @patch("deps.oai.batch_api.batch_api.OpenAI")
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_upload_batch_file(self, mock_file, mock_open_ai):
        """
        Test the upload_batch_file function to ensure it correctly uploads a file.

        Args:
            mock_file: Mock for the built-in open function.
            MockOpenAI: Mock for the OpenAI client.

        Asserts:
            The OpenAI client files.
            create method is called once with the correct parameters.
            The function returns the expected file ID.
        """
        mock_client = mock_open_ai.return_value
        mock_response = MagicMock()
        mock_response.id = "file-id"
        mock_client.files.create.return_value = mock_response

        file_path = "tests/mock_data.jsonl"
        result = upload_batch_file(file_path)

        mock_client.files.create.assert_called_once_with(
            file=mock_file.return_value, purpose="batch"
        )
        self.assertEqual(result, "file-id")

    @patch("deps.oai.batch_api.batch_api.OpenAI")
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_submit_batch_job(self, _, mock_open_ai):
        """
        Test the submit_batch_job function to ensure it correctly submits a batch job.

        Args:
            mock_file: Mock for the built-in open function.
            MockOpenAI: Mock for the OpenAI client.

        Asserts:
            The function returns the expected batch ID.
            The OpenAI client batches.
            create method is called once with the correct parameters.
        """
        mock_client = mock_open_ai.return_value
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
            metadata={"description": description},
        )

    @patch("deps.oai.batch_api.batch_api.OpenAI")
    def test_retrieve_batch_result(self, mock_open_ai):
        """
        Test the retrieve_batch_result function
        to ensure it correctly retrieves batch results.

        Args:
            MockOpenAI: Mock for the OpenAI client.

        Asserts:
            The OpenAI client files.
            content method is called once with the correct file ID.
            The function returns the expected response content.
        """
        mock_client = mock_open_ai.return_value
        mock_response = MagicMock()
        mock_client.files.content.return_value = mock_response

        file_id = "file-id"
        result = retrieve_batch_result(file_id)

        mock_client.files.content.assert_called_once_with(file_id)
        self.assertEqual(result, mock_response)

    @patch("deps.oai.batch_api.batch_api.OpenAI")
    def test_check_batch_status(self, mock_open_ai):
        """
        Test the check_batch_status function
        to ensure it correctly checks the batch status.

        Args:
            MockOpenAI: Mock for the OpenAI client.

        Asserts:
            The OpenAI client batches.
            retrieve method is called once with the correct batch ID.
            The function returns the expected batch status.
        """
        mock_client = mock_open_ai.return_value
        mock_response = MagicMock()
        mock_client.batches.retrieve.return_value = mock_response

        batch_id = "batch-id"
        result = check_batch_status(batch_id)

        mock_client.batches.retrieve.assert_called_once_with(batch_id=batch_id)
        self.assertEqual(result, mock_response)


if __name__ == "__main__":
    unittest.main()
