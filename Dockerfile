# Dockerfile for PenPaper Flask app
# Multi-arch base image (works on x86_64 and ARM/Raspberry Pi via manifest)
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.0

# Install system dependencies needed for Pillow and building wheels
RUN apt-get update \
     && apt-get install -y --no-install-recommends \
         build-essential \
         libjpeg62-turbo-dev \
         zlib1g-dev \
         libwebp-dev \
         libtiff5-dev \
         curl \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency manifest and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Install gunicorn for production serving
RUN pip install --no-cache-dir gunicorn

# Copy project
COPY . /app/

# Create a non-root user for running the app
RUN useradd -m -s /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=8000

EXPOSE 8000

# Copy start script and make executable
COPY --chown=appuser:appuser start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Healthcheck uses curl to probe the webroot
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

# Start script will initialize DB and exec gunicorn
CMD ["/app/start.sh"]
