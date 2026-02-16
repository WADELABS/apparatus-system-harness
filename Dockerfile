# Dockerfile for Apparatus System Harness
# Production-ready container image

FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY manifests/ ./manifests/

# Create directories for runtime data
RUN mkdir -p /app/artifacts /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    MANIFEST_DIR=/app/manifests \
    ARTIFACT_DIR=/app/artifacts

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command (can be overridden)
CMD ["python", "-m", "inquisitor.cli"]
