FROM python:3.10-slim

# System configuration environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# FIX: Install minimal system build utilities needed to compile wheels successfully
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optimize layer caching behavior for dependencies
COPY requirements.txt .

# Upgrade pip and pull in your updated, collision-free dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code folders into the container file system
COPY src/ src/
COPY models/ models/

EXPOSE 8000

# Continuous automated application health monitoring
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.agrivision.main:app", "--host", "0.0.0.0", "--port", "8000"]