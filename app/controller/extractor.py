import pandas as pd
from sqlalchemy import Engine
from typing import Generator

from utils.logger import get_logger

logger = get_logger()


class SQLExtractor:
    """
    Extracts data from a SQL database table in incremental chunks.

    This class connects to a SQL database using a SQLAlchemy engine
    and yields data in pandas DataFrames, suitable for processing large tables
    without loading the entire dataset into memory.
    """

    def __init__(
        self,
        engine: Engine,
        columns_to_select: list[str],
        schema_name: str,
        table_name: str,
        cursor_column: str,
        chunk_size: int = 1_000_000,
    ) -> None:
        """
        Initializes the SQLExtractor.

        Args:
            engine: An authenticated SQLAlchemy engine instance for the SQL database.
            columns_to_select: List of columns to use in select query.
            schema_name: The name of the database schema.
            table_name: The name of the table to extract data from.
            cursor_column: The name of the column to use as a cursor for incremental extraction.
            chunk_size: The number of rows to fetch in each chunk. Defaults to 1,000,000.
        """
        self.engine = engine
        self.columns_to_select = columns_to_select
        self.schema_name = schema_name
        self.table_name = table_name
        self.cursor_column = cursor_column
        self.chunk_size = chunk_size

    def _build_incremental_query(self, last_cursor: str) -> str:
        """
        Builds the SQL query for incremental data extraction.

        This private method constructs a query that selects all new rows
        from the source table based on a cursor value.

        Args:
            last_cursor: The last recorded value of the cursor column, used to
                         fetch only newer records.

        Returns:
            A string containing the complete SQL query.
        """
        columns = ", ".join(f'"{c}"' for c in self.columns_to_select)

        query = f"""
            SELECT {columns}
            FROM {self.schema_name}.{self.table_name}
            WHERE {self.cursor_column} > '{last_cursor}'
            ORDER BY {self.cursor_column} ASC
            """
        return query

    def extract_chunks(
        self, last_cursor: str
    ) -> Generator[tuple[int, pd.DataFrame], None, None]:
        """
        Extracts data from the database and yields it in chunks.

        This is a generator method that executes the incremental query and
        yields each chunk as a pandas DataFrame.

        Args:
            last_cursor: The starting cursor value for the incremental query.

        Yields:
            A pandas DataFrame for each chunk of data fetched from the database.
        """
        query = self._build_incremental_query(last_cursor)

        logger.info(
            f"Starting to extract chunks from table: '{self.table_name}' using column: '{self.cursor_column}' as cursor"
        )
        with self.engine.connect() as conn:
            try:
                chunk_iterator = pd.read_sql(
                    sql=query, con=conn, chunksize=self.chunk_size
                )

                for i, chunk in enumerate(chunk_iterator, 1):
                    if not chunk.empty:
                        try:
                            logger.info(f"Extracted chunk {i} with {len(chunk)} rows.")
                            yield i, chunk
                        except Exception:
                            logger.error("Error parsing iterator")
                            raise

            except Exception:
                logger.error("Error reading SQL Query")
                raise

            logger.info("Finished extracting all chunks from database.")