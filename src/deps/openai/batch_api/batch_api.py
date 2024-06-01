from openai import OpenAI

def get_openai_client():
    return OpenAI()

# Function to upload batch file
def upload_batch_file(file_path):
  client = OpenAI()

  response = client.files.create(
    file=open(file_path, "rb"),
    purpose="batch"
  )
  return response.id

def submit_batch_job(file_path, description):
  client = OpenAI()
  batch_input_file_id = upload_batch_file(file_path)
  response = client.batches.create(
    input_file_id=batch_input_file_id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={
      "description": description
    }
  )

  batch_id = response.id
  return batch_id

# Function to check job status and retrieve results
def retrieve_batch_result(file_id):
  client = OpenAI()
  return client.files.content(file_id)

def check_batch_status(batch_id):
  client = OpenAI()

  return client.batches.retrieve(batch_id=batch_id)