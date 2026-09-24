# ── Stage 1: Build dependencies and collect static files ──────────────────────
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

# Pre-compile .py → .pyc for faster container startup
ENV UV_COMPILE_BYTECODE=1
# Copy files instead of symlinking (required when source/dest are different filesystems)
ENV UV_LINK_MODE=copy

# Install dependencies first (this layer is cached until pyproject.toml changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-dev --no-install-project

# Copy the full project source
COPY . .

# Install the project package itself into the venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Collect static files into staticfiles/ (whitenoise will serve them)
ENV PATH="/app/.venv/bin:$PATH"
RUN python manage.py collectstatic --noinput


# ── Stage 2: Lean production image ────────────────────────────────────────────
FROM python:3.12-slim-bookworm

RUN addgroup --gid 1000 app && adduser --uid 1000 --ingroup app --disabled-password --gecos "" app

# gosu cleanly drops from root to app user inside the entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the built virtual environment and project from the builder stage
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app /app

# Put the venv's bin/ first on PATH so python/gunicorn resolve correctly
ENV PATH="/app/.venv/bin:$PATH"

RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh && \
    mkdir -p /app/data /app/media

# Container starts as root so the entrypoint can fix volume ownership
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
# 3 worker processes — a sensible default for a small/medium server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--worker-tmp-dir", "/dev/shm", "mainproject.wsgi:application"]
