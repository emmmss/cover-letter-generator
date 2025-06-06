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

# Install build tools
RUN yum install -y gcc python3-devel

# Optional: upgrade pip to get better wheel support
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY ./app ./app

# Set the handler
CMD ["app.main.lambda_handler"]