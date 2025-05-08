# src/synthetic_data.py

import os
import uuid
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text

# CONFIGURATION
NUM_CUSTOMERS = 500
NUM_ORDERS = 5000

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "rfm.db")
DDL_PATH = os.path.join(PROJECT_ROOT, "sql", "create_tables.sql")
EXTRACT_SQL_PATH = os.path.join(PROJECT_ROOT, "sql", "queries", "extract_orders.sql")

# Filenames for CSV outputs
CUSTOMERS_CSV = "customers.csv"
ORDERS_CSV = "orders.csv"
JOINED_CSV = "joined_orders.csv"


def make_data_dir():
    os.makedirs(RAW_DIR, exist_ok=True)


def generate_customers(n_customers: int = NUM_CUSTOMERS) -> pd.DataFrame:
    """Generate a table of customers with unique IDs and signup dates."""
    fake = Faker()
    customers = []
    for _ in range(n_customers):
        cust_id = str(uuid.uuid4())
        signup_date = fake.date_between(start_date='-2y', end_date='today')
        customers.append({
            "customer_id": cust_id,
            "signup_date": signup_date
        })
    return pd.DataFrame(customers)


def generate_orders(customers: pd.DataFrame, n_orders: int = NUM_ORDERS) -> pd.DataFrame:
    """Generate random orders tied to the given customers."""
    fake = Faker()
    orders = []
    customer_ids = customers["customer_id"].tolist()
    for _ in range(n_orders):
        order_id = str(uuid.uuid4())
        cust_id = random.choice(customer_ids)
        signup = customers.loc[customers["customer_id"] == cust_id, "signup_date"].values[0]
        order_date = fake.date_between(start_date=signup, end_date='today')
        order_amount = round(random.uniform(5.0, 500.0), 2)
        orders.append({
            "order_id": order_id,
            "customer_id": cust_id,
            "order_date": order_date,
            "order_amount": order_amount
        })
    return pd.DataFrame(orders)


def save_to_csv(df: pd.DataFrame, filename: str):
    path = os.path.join(RAW_DIR, filename)
    df.to_csv(path, index=False)
    print(f"Written {len(df):,} records to {path}")


def main():
    make_data_dir()

    # 1. Generate synthetic data
    print("Generating synthetic customers...")
    customers_df = generate_customers()
    print("Generating synthetic orders...")
    orders_df = generate_orders(customers_df)

    # 2. Connect to SQLite
    engine = create_engine(f"sqlite:///{DB_PATH}")
    print(f"Connecting to SQLite DB at {DB_PATH}...")

    # 3. Execute DDL to create tables using executescript
    with open(DDL_PATH, 'r') as f:
        ddl_sql = f.read()
    # Use raw DB-API connection for multi-statement execution
    raw_conn = engine.raw_connection()
    try:
        cursor = raw_conn.cursor()
        cursor.executescript(ddl_sql)
        raw_conn.commit()
        print("✅ Executed create_tables.sql via executescript")
    finally:
        raw_conn.close()

    # 4. Load data into tables
    customers_df.to_sql('customers', con=engine, if_exists='replace', index=False)
    print(f"Loaded {len(customers_df):,} customers into DB")
    orders_df.to_sql('orders', con=engine, if_exists='replace', index=False)
    print(f"Loaded {len(orders_df):,} orders into DB")

    # 5. Extract joined orders via extract_orders.sql
    with open(EXTRACT_SQL_PATH, 'r') as f:
        extract_sql = f.read()
    joined_df = pd.read_sql_query(text(extract_sql), con=engine)
    save_to_csv(joined_df, JOINED_CSV)
    print(f"✅ Extracted joined orders and saved to {JOINED_CSV}")

    print("🎉 Synthetic data generation and SQL pipeline complete.")


if __name__ == "__main__":
    main()
