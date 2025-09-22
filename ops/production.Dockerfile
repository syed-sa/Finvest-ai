# base image
FROM python:3.13-slim as base

FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.7.18 /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /code

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml /code/

# Compile bytecode
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project

# Copy remaining project files into the image
COPY . /code

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
