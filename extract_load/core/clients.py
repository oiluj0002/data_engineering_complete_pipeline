from sqlalchemy import create_engine, Engine, URL, NullPool
from boto3 import client
from mypy_boto3_s3 import S3Client

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

def get_s3_client() -> S3Client:
    """
    Creates and returns a Boto3 S3 client configured for the specified AWS bucket.

    It reads AWS access key, secret key, and endpoint URL from the config module.

    Returns:
        A Boto3 S3 client instance.

    Raises:
        Exception: If the S3 client creation fails.
    """

    try:
        s3_client = client(
            's3',
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            endpoint_url=env.AWS_ENDPOINT_URL
        )
        logger.info("S3 client created successfully.")
        return s3_client

    except Exception as e:
        logger.error(f"Failed to create S3 client. Error: {e}")
        raise