# src/data_engineering.py

import os
import pandas as pd
from sqlalchemy import create_engine

from .utils import ensure_dir, load_sql_query

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "rfm.db")
EXTRACT_SQL_PATH = os.path.join(PROJECT_ROOT, "sql", "queries", "extract_orders.sql")


def load_joined_data() -> pd.DataFrame:
    """
    Load orders joined with customer data from SQLite via SQL script.
    Returns a DataFrame with columns: order_id, customer_id, signup_date, order_date, order_amount.
    """
    ensure_dir(PROCESSED_DIR)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = load_sql_query(engine, EXTRACT_SQL_PATH)
    return df

def save_rfm(rfm_df: pd.DataFrame, filename: str = "rfm_scores.csv"):
    """
    Save the RFM DataFrame to CSV in processed folder.
    """
    ensure_dir(PROCESSED_DIR)
    path = os.path.join(PROCESSED_DIR, filename)
    rfm_df.to_csv(path, index=False)
    print(f"Saved RFM scores to {path}")