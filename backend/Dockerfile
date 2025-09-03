FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# (Optional) build tools for native deps; remove to keep slim if you don't need them
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 8000

# Healthcheck (expects GET /health to return 200)
# HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
#   CMD wget -qO- http://localhost:8000/health >/dev/null 2>&1 || exit 1

# If your ASGI app lives in main.py as `app`
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

