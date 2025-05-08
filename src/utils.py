# src/utils.py

import os
import pandas as pd
from sqlalchemy.engine.base import Engine


def ensure_dir(path: str):
    """
    Create directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)


def load_sql_query(engine: Engine, sql_path: str) -> pd.DataFrame:
    """
    Read SQL from file and execute, returning the result as a DataFrame.
    """
    with open(sql_path, 'r') as f:
        query = f.read()
    # pandas.read_sql_query accepts SQLAlchemy Engine or connection
    df = pd.read_sql_query(query, con=engine)
    return df


def parse_date_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Ensure a column is parsed as datetime.
    """
    df[col] = pd.to_datetime(df[col])
    return df


def chunk_dataframe(df: pd.DataFrame, chunk_size: int):
    """
    Yield chunks of the DataFrame of size chunk_size.
    """
    for start in range(0, len(df), chunk_size):
        yield df.iloc[start:start + chunk_size]
