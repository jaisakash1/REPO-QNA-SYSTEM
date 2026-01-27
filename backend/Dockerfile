# Use a lightweight Python base
FROM python:3.11-slim

# Set environment variables to keep Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Point HuggingFace cache to a specific directory
    HF_HOME=/app/cache

WORKDIR /app

# Install build dependencies (often needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# 1. Install CPU-only PyTorch (Critical for Render Free/Starter tier)
# This saves massive amounts of RAM and Disk space by skipping GPU libraries
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 2. Install the rest of the requirements
# (Make sure you removed pywin32 from requirements.txt first!)
RUN pip install --no-cache-dir -r requirements.txt

# 3. Pre-download the SentenceTransformer model during build
# This ensures the model is "baked in" and doesn't download on startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-en-v1.5')"

# Copy the rest of the application code
COPY . .

# Expose the port (Render sets the PORT env var, but this is good documentation)
EXPOSE 8000

# Start command
# Note: We use the array format and reference the backend package structure
CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]