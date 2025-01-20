# Layer with Python and some shared environment variables
FROM python:3.12-slim-bullseye AS python

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Layer for installing Python dependencies
FROM python AS dependencies

ENV VIRTUAL_ENV=/opt/venv \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12

# Add some libraries sometimes needed for building Python dependencies, e.g. gcc
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y \
    build-essential

# Copy our Python requirements here
COPY ./pyproject.toml .

# Install uv and Python dependencies
# Note: Turn off pip progress bar because it seemed to cause some issues on deployment
# Note: Using a virtualenv seems unnecessary, but it reduces the size of the resulting Docker image
RUN --mount=type=cache,target=/root/.cache/pip --mount=type=cache,target=/root/.cache/uv \
    python -m pip config --user set global.progress_bar off && \
    python -m pip --disable-pip-version-check --no-color --no-input install --upgrade pip uv && \
    uv venv /opt/venv && \
    uv pip install --requirement pyproject.toml


# Layer with only the Python dependencies needed for serving the app in production
FROM python AS production

# Copy over the code
COPY /sites /sites

# Copy over the virtualenv and add it to the path
COPY --from=dependencies /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV="/opt/venv"

# For local development of coltrane
# COPY /coltrane /coltrane
# ENV PYTHONPATH="/coltrane/src:/sites:${PYTHONPATH:-}"

WORKDIR /sites

EXPOSE 80

# Install curl, collect static assets, compress static assets
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update --fix-missing && \
    apt-get install --no-install-recommends -y curl wget && \
    python app.py collectstatic -v 2 --noinput && \
    python app.py compress

# HEALTHCHECK --interval=1m --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -Ssf -H "X-Forwarded-Host: adamghill.com" -o /dev/null http://0.0.0.0:80/static/css/sanitize.css || exit 1

# Run gunicorn
CMD ["gunicorn", "app:wsgi", "--config=gunicorn.conf.py"]
