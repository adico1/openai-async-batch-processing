FROM python:3.9-slim

ENV ENV_FILE_PATH .env

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app/src

# Ensure output is not buffered (important for Docker logs)
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/batch_processor.py"]
