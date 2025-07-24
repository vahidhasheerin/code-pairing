FROM python:3.9.18-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_PORT=8080

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    # Remove pip cache and unnecessary files
    && apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Create and use a non-root user
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser /app
USER appuser

# Expose parameterized port
EXPOSE ${APP_PORT}

# Healthcheck endpoint
HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:${APP_PORT}/health || exit 1

#Command to run the application
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${APP_PORT} app:app"]
