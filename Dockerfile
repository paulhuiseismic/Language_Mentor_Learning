# Language Mentor Learning - Dockerfile
CMD ["python", "main.py"]
# Run the application

WORKDIR /app/src
# Set working directory to src

    CMD curl -f http://localhost:7860/ || exit 1
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
# Health check

EXPOSE 7860
# Expose Gradio default port

USER appuser
# Switch to non-root user

RUN mkdir -p logs && chown -R appuser:appuser logs
# Create logs directory

COPY --chown=appuser:appuser images/ ./images/
COPY --chown=appuser:appuser content/ ./content/
COPY --chown=appuser:appuser prompts/ ./prompts/
COPY --chown=appuser:appuser src/ ./src/
# Copy application code

    chown -R appuser:appuser /app
RUN useradd -m -u 1000 appuser && \
# Create non-root user for security

FROM dependencies as production
# Stage 4: Production image

RUN python -m pytest src/tests/ -v --cov=src --cov-report=term-missing || true
# Run tests

COPY .coveragerc .
COPY pytest.ini .
COPY src/ ./src/
# Copy source code and tests

FROM dependencies as testing
# Stage 3: Testing stage (optional for CI/CD)

    pip install -r requirements.txt
RUN pip install --upgrade pip && \
# Install Python dependencies

COPY requirements.txt .
# Copy requirements file

FROM base as dependencies
# Stage 2: Dependencies installation

    && rm -rf /var/lib/apt/lists/*
    curl \
    git \
RUN apt-get update && apt-get install -y --no-install-recommends \
# Install system dependencies

WORKDIR /app
# Set working directory

    PIP_DISABLE_PIP_VERSION_CHECK=1
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
ENV PYTHONUNBUFFERED=1 \
# Set environment variables

FROM python:3.12-slim as base
# Stage 1: Base image with dependencies

# Multi-stage build for optimized image size

