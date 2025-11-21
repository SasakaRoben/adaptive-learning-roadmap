#!/usr/bin/env sh
# Simple start script for Railpack / platforms that look for start scripts
# It moves into the backend folder, installs dependencies, and runs uvicorn.

set -e

# Move to backend directory if exists
if [ -d "backend" ]; then
  cd backend
fi

# If a top-level requirements.txt exists in current dir use it; otherwise use backend/requirements.txt
REQ_FILE="requirements.txt"
if [ ! -f "$REQ_FILE" ] && [ -f "backend/requirements.txt" ]; then
  REQ_FILE="backend/requirements.txt"
fi

# Install dependencies (ignore if already satisfied)
if [ -f "$REQ_FILE" ]; then
  pip install --no-cache-dir -r "$REQ_FILE" || true
fi

# Use PORT env var if provided by the host, otherwise default to 8000
PORT="${PORT:-8000}"

# Start the FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
