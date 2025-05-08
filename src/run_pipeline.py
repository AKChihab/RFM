# src/run_pipeline.py

"""
End-to-end pipeline script showing how to use utils and data_engineering modules:
 1. Load joined orders from SQLite
 2. Parse date columns
 3. Compute RFM scores
 4. Save RFM output
"""
import os

def main():
    # Imports
    from src.utils import parse_date_column, ensure_dir
    from src.data_engineering import load_joined_data, save_rfm
    from src.rfm import compute_rfm
    # 1. Load joined orders
    print("Loading joined orders...")
    orders_df = load_joined_data()

    # 2. Ensure date columns are proper datetimes
    print("Parsing date columns...")
    orders_df = parse_date_column(orders_df, "signup_date")
    orders_df = parse_date_column(orders_df, "order_date")

    # 3. Compute RFM
    print("Computing RFM scores...")
    rfm_df = compute_rfm(orders_df)

    # 4. Save RFM output
    print("Saving RFM results...")
    save_rfm(rfm_df)

    print("Pipeline complete!")

if __name__ == "__main__":
    main()
