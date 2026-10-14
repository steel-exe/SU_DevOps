# =============================================================================
# Dockerfile: Enterprise Student Record & Academic Management Platform
# Multi-stage lightweight Python 3.10 production container
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build Dependencies
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS builder

WORKDIR /build

# Install build-time dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies to virtual wheel store
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Runtime Environment
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS runner

# Set metadata and environment flags
LABEL maintainer="SU_DevOps Engineering Team"
LABEL description="Student Record and Academic Management Microservice"
LABEL version="1.0.0"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000 \
    PATH=/home/appuser/.local/bin:$PATH

# Install curl for container health check
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user and group for defense-in-depth
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# Set working directory
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local

# Copy application source code
COPY --chown=appuser:appgroup app/ /app/app/

# Switch to non-root user
USER appuser

# Expose microservice port
EXPOSE 5000

# Container liveness health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Launch production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--access-logfile", "-", "--error-logfile", "-", "app.main:app"]
