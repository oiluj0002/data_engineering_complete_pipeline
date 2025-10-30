import io
import uuid
import pandas as pd

from utils.logger import get_logger
from core.clients import get_db_engine, get_s3_client

logger = get_logger()


def extract_table(schema: str, table: str) -> pd.DataFrame:
    engine = get_db_engine()
    query = f"SELECT * FROM {schema}.{table};"

    with engine.connect() as conn:
        try:
            df = pd.read_sql(query, conn)
            logger.info(f"Extracted data from {schema}.{table}")
            return df
        except Exception as e:
            logger.error(f"Error extracting data from {schema}.{table}: {e}")
            raise

def upload_to_s3(bucket: str, key: str, data: pd.DataFrame) -> None:
    """
    Upload a DataFrame as Parquet to S3, handling UUID/object columns safely.

    Notes:
    - pandas.to_parquet returns None when writing to a file-like object. Use a BytesIO buffer.
    - Convert UUID object columns to string to avoid pyarrow dtype inference errors.
    """
    s3_client = get_s3_client()

    df = data.copy()
    # Convert UUID-typed object columns to string
    for col in df.columns:
        if df[col].dtype == object:
            series = df[col].dropna()
            if not series.empty and isinstance(series.iloc[0], uuid.UUID):
                df[col] = df[col].astype(str)

    buf = io.BytesIO()
    df.to_parquet(buf, engine="pyarrow", compression="snappy", index=False)
    buf.seek(0)

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=key,
            Body=buf.getvalue(),
            ContentType="application/octet-stream",
        )
        logger.info(f"Uploaded data to s3://{bucket}/{key}")
    except Exception as e:
        logger.error(f"Error uploading data to s3://{bucket}/{key}: {e}")
        raise