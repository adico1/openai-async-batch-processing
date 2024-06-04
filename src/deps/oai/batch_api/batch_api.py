"""
Module for handling batch file operations with the OpenAI API.

This module includes functions to:
- Upload a batch file.
- Submit a batch job.
- Retrieve batch results.
- Check batch job status.
"""

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Get an instance of the OpenAI client.

    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return OpenAI()


def upload_batch_file(file_path: str) -> str:
    """
    Upload a batch file to OpenAI.

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        str: The ID of the uploaded file.
    """
    client = OpenAI()
    with open(file_path, "rb") as file:
        response = client.files.create(file=file, purpose="batch")
    return response.id


def submit_batch_job(file_path: str, description: str) -> str:
    """
    Submit a batch job to OpenAI.

    Args:
        file_path (str): The path to the input file for the batch job.
        description (str): A description for the batch job.

    Returns:
        str: The ID of the submitted batch job.
    """
    client = OpenAI()
    batch_input_file_id = upload_batch_file(file_path)
    response = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": description},
    )
    batch_id = response.id
    return batch_id


def retrieve_batch_result(file_id: str) -> bytes:
    """
    Retrieve the content of a batch result file from OpenAI.

    Args:
        file_id (str): The ID of the file to retrieve.

    Returns:
        bytes: The content of the file.
    """
    client = OpenAI()
    return client.files.content(file_id)


def check_batch_status(batch_id: str) -> dict:
    """
    Check the status of a batch job in OpenAI.

    Args:
        batch_id (str): The ID of the batch job to check.

    Returns:
        dict: The status of the batch job.
    """
    client = OpenAI()
    return client.batches.retrieve(batch_id=batch_id)
