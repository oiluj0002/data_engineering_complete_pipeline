import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# --- Database ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# --- Extraction Values ---
EXECUTION_TS = os.getenv("EXECUTION_TS", "1900-01-01 00:00:00.000000")
CLOUD_RUN_TASK_INDEX = int(os.getenv("CLOUD_RUN_TASK_INDEX", 0))