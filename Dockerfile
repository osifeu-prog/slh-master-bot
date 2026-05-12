FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y docker.io curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY slh_master_bot.py .
COPY bsc_client.py .
# No .env copy - Railway injects variables directly
CMD ["python", "-u", "slh_master_bot.py"]

