# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set environment variables for Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$POETRY_HOME/bin:$PATH"

# Set the working directory in the container
WORKDIR /usr/src/app

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Install package poetry
RUN pip install poetry==1.8.5

# Poetry install
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy the rest of the application code into the container
COPY . ./

# PORT is automatically provided by Cloud Run, typically 8080
# EXPOSE 8080

# Run the web service on container startup
# Set desired Gunicorn worker count (adjust based on Cloud Run CPU/Memory and expected load)
# Cloud Run v2 usually provides at least 1 CPU, v1 might share, start with 1 or 2
# Use Uvicorn as the worker class for async support
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling
CMD exec gunicorn \
    --bind :$PORT \
    --workers 1 \
    --threads 4 \
    --timeout 0 \
    --worker-class uvicorn.workers.UvicornWorker \
    pjecz_casiopea_api_oauth2.main:app
