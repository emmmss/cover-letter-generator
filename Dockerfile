# ===== Stage 1: Base for development =====
FROM python:3.11-slim AS dev

WORKDIR /app

# Install build tools and dependencies for native packages
RUN apt-get update && apt-get install -y \
    build-essential gcc \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ===== Stage 2: Lambda-compatible image =====
FROM public.ecr.aws/lambda/python:3.11 AS lambda

# Set working directory for Lambda
WORKDIR /var/task

# Copy from dev stage
COPY --from=dev /app /var/task
COPY requirements.txt .

# Install deps again in Lambda env
RUN pip install --no-cache-dir -r requirements.txt

# Lambda entrypoint (FastAPI adapter)
CMD ["app.main.handler"]