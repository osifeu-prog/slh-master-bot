FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y docker.io curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY slh_master_bot.py .
# COPY .env .   <--- הסר שורה זו
COPY .env.example .env   # יצור .env ריק אם לא קיים
CMD ["python", "-u", "slh_master_bot.py"]

