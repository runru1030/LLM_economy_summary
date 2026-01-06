FROM python:3.12-slim-bookworm as builder

RUN pip install --upgrade pip && \
    pip install poetry==1.8.*

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --no-root

FROM python:3.12-slim-bookworm

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.user_interface.restapi:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log", "--no-use-colors", "--log-level", "warning"]
