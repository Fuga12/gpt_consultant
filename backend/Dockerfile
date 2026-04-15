FROM python:3.12-slim

WORKDIR /srv

COPY pyproject.toml uv.lock ./
COPY app ./app

RUN pip install --no-cache-dir uv && uv sync --no-dev

CMD ["uv", "run", "python", "-m", "app"]
