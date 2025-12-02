FROM python:3.12.3-slim

WORKDIR .

COPY /bot/requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

COPY /bot /bot

CMD ["python", "bot/bot.py"]