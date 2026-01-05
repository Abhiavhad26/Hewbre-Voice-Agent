FROM python:3.11-slim

WORKDIR /app

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the whole project
COPY . .

# 3. Install phonikud-tts as a local package
RUN pip install .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


