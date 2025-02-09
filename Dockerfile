FROM python3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "--port", "8000"]
