import os
import sys
import traceback
from fastapi import FastAPI

# Ensure the repository root (and legacy backend folder) are importable when
# Vercel runs from the project root. This lets `import app.main` resolve when
# the `app/` package is at the repository root.
ROOT = os.path.dirname(os.path.dirname(__file__))
# Add repo root first so top-level `app` package is found
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# Also add legacy `backend/` path for older layouts that put the package there
BACKEND_PATH = os.path.join(ROOT, 'backend')
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)


# Try to import the real FastAPI app. If import fails (missing deps, env,
# or other runtime errors), create a minimal fallback app that returns
# a clear error and prints the traceback to stderr so Vercel logs show it.
try:
    from app.main import app  # type: ignore
except Exception:
    tb = traceback.format_exc()
    # Print full traceback to stderr (Vercel will capture this in function logs)
    print("Failed to import backend FastAPI app:\n" + tb, file=sys.stderr)

    # Fallback app
    app = FastAPI(title="Fallback - import error")

    @app.get("/", tags=["health"])
    async def fallback_root():
        return {
            "message": "Backend import failed. Check server logs for traceback.",
            "error": True,
        }

    @app.get("/__import_traceback", include_in_schema=False)
    async def import_traceback():
        # Return a short portion of the traceback to help debugging (not full dump)
        return {"traceback": tb.splitlines()[-20:]}


# Vercel expects the ASGI application to be exposed as `app` in this module
__all__ = ["app"]
