import pandas as pd
import io
import uuid

from utils.logger import get_logger
from core.clients import (get_db_engine, get_s3_client)

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

def transform(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()

    # Convert UUID-typed object columns to string
    for col in df.columns:
        if df[col].dtype == object:
            series = df[col].dropna()
            if not series.empty and isinstance(series.iloc[0], uuid.UUID):
                df[col] = df[col].astype(str)

    logger.info("Transforming data")
    return df

def upload_to_s3(bucket: str, key: str, data: pd.DataFrame) -> None:
    s3_client = get_s3_client()
    
    buffer = io.BytesIO()
    data.to_parquet(path=buffer, engine="pyarrow", compression="snappy", index=False)
    buffer.seek(0)

    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=buffer, ContentType="application/octet-stream")
        logger.info(f"Uploaded data to s3://{bucket}/{key}")
    except Exception as e:
        logger.error(f"Error uploading data to s3://{bucket}/{key}: {e}")
        raise

if __name__ == "__main__":
    schema_name = "public"
    table_name = "wallets"
    bucket_name = "s3-bucket-test"
    s3_key = "data/wallets.parquet"

    try:
        data_frame = extract_table(schema_name, table_name)
        transformed_data = transform(data_frame)
        upload_to_s3(bucket_name, s3_key, transformed_data)
        logger.info("Data extraction and upload completed successfully.")
    except Exception as e:
        logger.error(f"Process failed: {e}")