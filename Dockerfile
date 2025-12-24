# Simplified Dockerfile for Baratie Food Ordering System
# Supports both frontend and backend services

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
CMD if [ "$SERVICE_NAME" = "frontend" ]; then \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5001} frontend.app:app; \
    else \
        gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} backend.app:app; \
    fi
