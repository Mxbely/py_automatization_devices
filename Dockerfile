ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies.
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Copy dependency files
COPY ./poetry.lock /poetry.lock
COPY ./pyproject.toml /pyproject.toml

# Configure Poetry to avoid creating a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies with Poetry
RUN poetry lock
RUN poetry install --no-root --only main

# Copy the source code into the container.
COPY . .

# Run the application.
CMD ["poetry", "run", "python", "logging/do_it_yourself.py"]
