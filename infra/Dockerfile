FROM python:3.10-slim

# Set environment variables
# Try to match poetry version with the one in nix/packages.nix
ENV POETRY_VERSION=1.3.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry
# Pin versions in apt-get install, set SHELL option -o pipefail, and consolidate RUN instructions
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        curl=7.* \
        build-essential=12.* \
        libffi-dev=3.* \
        wkhtmltopdf=0.12.* && \
        # libssl-dev=1.* && \
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python - && \
    # Cleanup
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the project files
WORKDIR /app

COPY ./pyproject.toml ./

# Install the dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

ENV PYTHONPATH /app:$PYTHONPATH

# Copy the current directory to WORKDIR
COPY . .
RUN rm -rf /app/notebooks

CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--chdir", "src", "main:flask_app",  "--timeout", "30", "--access-logfile",  "-"]
