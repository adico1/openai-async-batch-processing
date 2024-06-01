# OpenAI Batch SDK

This library provides a simple interface for integrating OpenAI ChatGPT batch processing into any Python development environment. It supports event-driven architecture, making it easy to handle batch job completions.

(Note: Read The License Disclaimer about code status and AI assited coding)

## Installation

```bash
pip install openai_batch_sdk
```

## Example Code for Usage
```python
from openai_batch_sdk import start_monitoring, EventHandler, send_notification, retrieve_batch_results

# Initialize event handler
event_handler = EventHandler()
event_handler.register_event("batch_completed", send_notification)

# Start monitoring the batch job
start_monitoring("/app/path_to_your_file.jsonl", event_handler)
```

## Development

### Building the Project

1. Navigate to the Project Directory:

```bash
cd /path/to/openai_batch_sdk
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Build the Package:
```bash
python setup.py sdist bdist_wheel
```

### Testing the Project
1. Navigate to the Tests Directory:
```bash
cd /path/to/openai_batch_sdk/tests
```
2. Run the Tests:
```bash
python -m unittest discover
```

### Running the Project
1. Create a Docker Image:
```bash
docker build -t openai_batch_sdk:latest /path/to/openai_batch_sdk
```
2. Run the Docker Container:
```bash
docker run -d openai_batch_sdk:latest
```

### Deploying to Kubernetes
1. Apply the Kubernetes Configuration:
```bash
kubectl apply -f /path/to/openai_batch_sdk/k8s-deployment.yaml
```

## License
MIT License (Read The Disclaimer)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Disclaimer: This project is a draft and has not been battle-tested. Use at your own risk. The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

Generated with the help of ChatGPT.