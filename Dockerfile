FROM python:3.9.6-slim-buster AS base

WORKDIR /app/src

RUN pip install poetry==1.4.0

COPY . /app/src/

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# For Development
FROM base AS app-dev

RUN apt update && apt upgrade -y && apt install git make zsh curl vim ssh -y

RUN poetry install

CMD ["uvicorn", "app.application:get_app", "--host", "0.0.0.0", "--port", "8000"]

# For Deployment
FROM base as release
ENV LOG_LEVEL=INFO
CMD ["uvicorn", "app.application:get_app", "--host", "0.0.0.0", "--port", "8000"]