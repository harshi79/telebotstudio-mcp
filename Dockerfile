FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and documentation
COPY . .

# Render assigns PORT dynamically; --host and --port defaults read HOST/PORT env vars
CMD ["python", "server.py", "--transport", "http"]
