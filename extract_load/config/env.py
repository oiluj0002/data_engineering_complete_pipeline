import os

try:
    # Load variables from a .env file when available (no hard dependency in prod)
    from dotenv import load_dotenv

    load_dotenv("extract_load/secret/.env")
except ImportError:
    pass

_REQUIRED_VARS = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_ENDPOINT_URL",
]

_missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
if _missing:
    raise EnvironmentError(
        f"Missing required environment variables: {', '.join(_missing)}"
    )

# --- Database ---
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_NAME = os.environ["DB_NAME"]

# --- AWS ---
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_ENDPOINT_URL = os.environ["AWS_ENDPOINT_URL"]