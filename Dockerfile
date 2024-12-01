FROM python:3.12-slim AS builder

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --quiet --no-cache-dir build && \
    pip install --quiet --no-cache-dir .

COPY aegis/ aegis/

FROM python:3.12-slim

WORKDIR /app

RUN groupadd --gid 1001 aegis && \
    useradd --uid 1001 --gid aegis --no-create-home aegis

COPY --from=builder /app /app

USER aegis

EXPOSE 8000

CMD ["uvicorn", "aegis.main:app", "--host", "0.0.0.0", "--port", "8000"]
