FROM python:3.12-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.11.16 /uv /usr/local/bin/uv
WORKDIR /opt/app

# ----- Restore python packages -----
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock .python-version /opt/app/
RUN uv sync --frozen --no-dev

# ----- Copy all files -----
COPY ./ /opt/app/
COPY ./core/local_settings.py.production /opt/app/core/local_settings.py
RUN mkdir -p /opt/app/db /opt/app/log

CMD ["bash", "-c", "python manage.py migrate && python manage.py increment"]
