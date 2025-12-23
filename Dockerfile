# Multi-Service Dockerfile for Baratie Food Ordering System
# Build argument determines which service to run

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (will be overridden by $PORT in production)
EXPOSE 5000

# Default command - can be overridden in docker-compose or Render
# Use SERVICE_NAME environment variable to determine which service to run
CMD if [ "$SERVICE_NAME" = "gateway" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} api_gateway.app:app; \
    elif [ "$SERVICE_NAME" = "frontend" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} frontend.app:app; \
    elif [ "$SERVICE_NAME" = "core" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5002} core_service.app:app; \
    elif [ "$SERVICE_NAME" = "transaction" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5003} transaction_service.app:app; \
    else \
        echo "Error: SERVICE_NAME not set. Use: gateway, frontend, core, or transaction"; \
        exit 1; \
    fi
