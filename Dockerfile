FROM python:3.9.6-slim-buster AS base

WORKDIR /app/src

RUN pip install poetry==1.3.2

COPY pyproject.toml poetry.lock /app/src/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root

ENV PYTHONPATH=/app/src

# For Development
FROM base AS app-dev

WORKDIR /app/src

COPY . /app/src/

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    zsh \
    curl \
    vim \
    ssh \
    && rm -rf /var/lib/apt/lists/*

RUN poetry install

# For Deployment
FROM base AS release

WORKDIR /app/src

COPY . /app/src/

ENV LOG_LEVEL=INFO
CMD ["uvicorn", "app.application:get_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
