FROM python:3.12-slim

ENV POETRY_HOME="/opt/poetry" \ 
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=true \
    PATH="/opt/poetry/bin:$PATH"

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry


WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["python", "app/main.py"]
