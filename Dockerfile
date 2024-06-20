# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Verify Poetry installation
RUN poetry --version

# Set the working directory
WORKDIR /

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . .

# Set the entrypoint for the container
ENTRYPOINT ["poetry", "run", "python", "main.py"]