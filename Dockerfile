FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install --only main --no-root

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "spot2_challenge.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]