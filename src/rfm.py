# src/rfm.py

"""
Module for computing RFM (Recency, Frequency, Monetary) scores and segments.
"""
import pandas as pd


def compute_rfm(
    df: pd.DataFrame,
    snapshot_date: pd.Timestamp = None
) -> pd.DataFrame:
    """
    Compute RFM metrics and assign scores:
      - Recency: days since last purchase (smaller is better)
      - Frequency: number of orders (higher is better)
      - Monetary: total spend (higher is better)

    Returns a DataFrame with columns:
      customer_id, recency_days, frequency, monetary, R, F, M, rfm_segment, rfm_score
    """
    # Ensure order_date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['order_date']):
        df['order_date'] = pd.to_datetime(df['order_date'])

    # Determine snapshot_date
    if snapshot_date is None:
        snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)

    # Aggregate R, F, M
    rfm = (
        df.groupby('customer_id')
          .agg(
              recency_days=('order_date', lambda x: (snapshot_date - x.max()).days),
              frequency=('order_id', 'count'),
              monetary=('order_amount', 'sum')
          )
          .reset_index()
    )

    # Score on 1-5 scale
    rfm['R'] = pd.qcut(rfm['recency_days'], 5, labels=[5,4,3,2,1]).astype(int)
    rfm['F'] = pd.qcut(rfm['frequency'],   5, labels=[1,2,3,4,5]).astype(int)
    rfm['M'] = pd.qcut(rfm['monetary'],    5, labels=[1,2,3,4,5]).astype(int)

    # Build segment and score
    rfm['rfm_segment'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)
    rfm['rfm_score']   = rfm[['R','F','M']].sum(axis=1)

    return rfm
