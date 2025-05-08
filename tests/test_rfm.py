import pandas as pd
import pytest
from src.rfm import compute_rfm

def make_sample_df():
    return pd.DataFrame([
        # customer A: two orders
        {"customer_id": "A", "order_id": 1, "order_date": pd.Timestamp("2025-05-01"), "order_amount": 100},
        {"customer_id": "A", "order_id": 2, "order_date": pd.Timestamp("2025-05-03"), "order_amount": 150},
        # customer B: one order
        {"customer_id": "B", "order_id": 3, "order_date": pd.Timestamp("2025-05-02"), "order_amount": 50},
    ])

def test_compute_rfm_basic():
    df = make_sample_df()
    # use a fixed snapshot date for predictability
    snapshot = pd.Timestamp("2025-05-04")
    rfm = compute_rfm(df, snapshot_date=snapshot)

    # recency_days: A → 1 (last on 05-03), B → 2 (last on 05-02)
    assert rfm.loc[rfm.customer_id=="A", "recency_days"].iloc[0] == 1
    assert rfm.loc[rfm.customer_id=="B", "recency_days"].iloc[0] == 2

    # frequency: A → 2, B → 1
    assert rfm.set_index("customer_id").loc["A", "frequency"] == 2
    assert rfm.set_index("customer_id").loc["B", "frequency"] == 1

    # monetary: A → 250, B → 50
    assert rfm.set_index("customer_id").loc["A", "monetary"] == 250
    assert rfm.set_index("customer_id").loc["B", "monetary"] == 50

    # R, F, M scores should be between 1–5
    assert all(rfm["R"].between(1,5))
    assert all(rfm["F"].between(1,5))
    assert all(rfm["M"].between(1,5))

    # segment string is concatenation
    seg_A = rfm.set_index("customer_id").loc["A", "rfm_segment"]
    seg_B = rfm.set_index("customer_id").loc["B", "rfm_segment"]
    assert isinstance(seg_A, str) and len(seg_A)==3
    assert isinstance(seg_B, str) and len(seg_B)==3
