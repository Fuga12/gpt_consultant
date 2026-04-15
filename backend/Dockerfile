FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY pyproject.toml uv.lock ./
COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && pip install --no-cache-dir uv \
    && uv sync --no-dev

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
