import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def retrieve_batch_results(batch_id):
    batch = openai.Batch.retrieve(batch_id)
    results = batch['results']
    return [result['content'] for result in results]
