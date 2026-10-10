FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN groupadd -g 10001 appuser && useradd -u 10001 -g appuser -s /bin/sh appuser
COPY --from=builder /install /usr/local
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser:appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
