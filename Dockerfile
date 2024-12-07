FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY . /app

EXPOSE 8080

CMD ["python", "src/main.py"]