FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/app/cache

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy requirements to the root of /app first (for caching)
COPY requirements.txt .

# 2. Install CPU-only PyTorch (Crucial for Render Free Tier)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 4. Pre-download the model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-base-en-v1.5')"

# ----------------- CRITICAL FIX -----------------
# Instead of copying files to root (COPY . .), we copy them into a 'backend' folder.
# This restores the structure "backend/api/..." that your code expects.
COPY . backend/

# Tell Python to look in /app so it can find the 'backend' package
ENV PYTHONPATH=/app
# ------------------------------------------------

EXPOSE 8000

# 5. Start command (Note: We use 'backend.api.main:app' again)
CMD ["sh", "-c", "uvicorn backend.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]