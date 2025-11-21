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


def _load_env_file(path: str) -> None:
    """Lightweight dotenv loader: reads KEY=VALUE lines and sets os.environ.
    Does not overwrite existing environment variables.
    """
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = val
    except FileNotFoundError:
        return
    except Exception:
        # avoid breaking imports for minor parse issues
        return


# Try to import the real FastAPI app. If import fails (missing deps, env,
# or other runtime errors), create a minimal fallback app that returns
# a clear error and prints the traceback to stderr so Vercel logs show it.
try:
    # If a local `backend/.env` exists during development, load it so
    # pydantic Settings (which reads `.env`) can find required vars when
    # importing from the repo root (useful for local tests).
    local_env = os.path.join(BACKEND_PATH, '.env')
    if os.path.exists(local_env):
        _load_env_file(local_env)

    from app.main import app  # type: ignore
except Exception:
    tb = traceback.format_exc()
    # Print full traceback to stderr (Vercel will capture this in function logs)
    print("Failed to import backend FastAPI app:\n" + tb, file=sys.stderr)

    # Try to extract missing-fields from Pydantic ValidationError if present
    missing_fields = None
    try:
        # Attempt to import pydantic here in case it's available in the traceback
        import pydantic
        # Walk the traceback to find the exception object
    except Exception:
        pydantic = None

    # Heuristic: look for lines mentioning "Field required" or ValidationError
    missing = []
    for line in tb.splitlines():
        if 'Field required' in line:
            # previous line often contains the field name in tracebacks; collect nearby words
            missing.append(line.strip())
    if missing:
        missing_fields = missing

    # Fallback app
    app = FastAPI(title="Fallback - import error")

    @app.get("/", tags=["health"])
    async def fallback_root():
        resp = {
            "message": "Backend import failed. Check server logs for traceback.",
            "error": True,
        }
        if missing_fields:
            resp["missing_env"] = missing_fields
        return resp

    @app.get("/__import_traceback", include_in_schema=False)
    async def import_traceback():
        # Return a short portion of the traceback to help debugging (not full dump)
        return {"traceback": tb.splitlines()[-40:], "missing_env": missing_fields}


# Vercel expects the ASGI application to be exposed as `app` in this module
__all__ = ["app"]
