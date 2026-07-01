FROM python:3.11.12-slim

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and documentation
COPY . .

# Run as non-root user for security
RUN useradd --create-home --shell /bin/false appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check: hit the /health endpoint managed by FastMCP/Starlette
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/health')" || exit 1

# Render assigns PORT dynamically; --host and --port defaults read HOST/PORT env vars
CMD ["python", "server.py", "--transport", "http"]
