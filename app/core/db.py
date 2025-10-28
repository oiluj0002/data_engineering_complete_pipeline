from sqlalchemy import create_engine, Engine, URL, NullPool

from config import env
from utils.logger import get_logger

logger = get_logger()


def get_db_engine() -> Engine:
    """
    Creates and returns a SQLAlchemy Engine instance for the database.

    It reads connection details from the config module.

    Returns:
        An authenticated SQLAlchemy Engine instance.

    Raises:
        Exception: If the database connection fails.
    """
    try:
        connection_url = URL.create(
            "postgresql+psycopg",
            username=env.DB_USER,
            password=env.DB_PASSWORD,
            host=env.DB_HOST,
            port=5432,
            database=env.DB_NAME
        )

        engine = create_engine(connection_url, poolclass=NullPool)
        logger.info("Database engine created successfully.")
        return engine

    except Exception as e:
        logger.error(f"Failed to create database engine. Error: {e}")
        raise