FROM python:3.12.3-slim

WORKDIR .
COPY /server/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY /server /server
ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]