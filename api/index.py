import os
import sys

# Ensure backend package is importable when Vercel runs from repo root
ROOT = os.path.dirname(os.path.dirname(__file__))
BACKEND_PATH = os.path.join(ROOT, 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

# Import the FastAPI app from backend/app/main.py
try:
    from app.main import app
except Exception as e:
    # If import fails, raise a clear error for Vercel logs
    raise

# Vercel expects the ASGI application to be exposed as `app` in this module
__all__ = ['app']
