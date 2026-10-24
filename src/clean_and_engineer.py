"""
Phase 2 & 3: Data Cleaning and Feature Engineering Pipeline
Handles deduplication, non-negative filtering, temporal reindexing (MultiIndex zero-fill),
and leakage-free time-series feature engineering (lags and rolling statistics).
"""

import os
import pandas as pd
import numpy as np

def load_raw_data(data_dir="data"):
    sales_path = os.path.join(data_dir, "sales.csv")
    inv_path = os.path.join(data_dir, "inventory.csv")
    del_path = os.path.join(data_dir, "deliveries.csv")
    
    sales = pd.read_csv(sales_path, parse_dates=["date"])
    inventory = pd.read_csv(inv_path, parse_dates=["date"])
    deliveries = pd.read_csv(del_path, parse_dates=["date"])
    
    return sales, inventory, deliveries

def clean_sales_data(sales):
    """
    Cleans raw sales records:
    1. Removes negative units (returns/adjustments).
    2. Drops duplicate records across (date, sku_id, warehouse_id).
    3. Reindexes over full Cartesian product of (dates x SKUs x warehouses) with 0 fill.
    """
    initial_rows = len(sales)
    
    # 1. Non-negative filter
    sales_clean = sales[sales["units_sold"] >= 0].copy()
    negatives_removed = initial_rows - len(sales_clean)
    
    # 2. Deduplication
    dups_count = sales_clean.duplicated(["date", "sku_id", "warehouse_id"]).sum()
    sales_clean = sales_clean.drop_duplicates(["date", "sku_id", "warehouse_id"])
    
    # Preserve SKU price lookup for filling
    price_lookup = sales_clean.groupby("sku_id")["unit_price"].median().to_dict()
    
    # 3. Full grid temporal reindexing
    date_range = pd.date_range(sales_clean["date"].min(), sales_clean["date"].max(), freq="D")
    skus = sorted(sales_clean["sku_id"].unique())
    warehouses = sorted(sales_clean["warehouse_id"].unique())
    
    full_index = pd.MultiIndex.from_product(
        [date_range, skus, warehouses],
        names=["date", "sku_id", "warehouse_id"]
    )
    
    daily = (sales_clean.set_index(["date", "sku_id", "warehouse_id"])
             .reindex(full_index, fill_value=0)
             .reset_index())
    
    # Re-apply unit prices for zero-fill rows
    daily["unit_price"] = daily["unit_price"].replace(0, np.nan)
    daily["unit_price"] = daily["unit_price"].fillna(daily["sku_id"].map(price_lookup))
    
    print(f"Cleaning Report:")
    print(f" - Initial rows: {initial_rows}")
    print(f" - Negative units dropped: {negatives_removed}")
    print(f" - Duplicate records removed: {dups_count}")
    print(f" - Balanced grid records after zero-fill: {len(daily)}")
    
    return daily

def add_time_features(daily_df):
    """
    Creates leakage-free lag and rolling features.
    Uses shift(1) prior to rolling calculations so target day value is never leaked.
    """
    df = daily_df.sort_values(["sku_id", "warehouse_id", "date"]).copy()
    g = df.groupby(["sku_id", "warehouse_id"])["units_sold"]
    
    df["lag_7"] = g.shift(7)
    df["lag_14"] = g.shift(14)
    df["roll_mean_7"] = g.transform(lambda s: s.shift(1).rolling(7).mean())
    df["roll_mean_28"] = g.transform(lambda s: s.shift(1).rolling(28).mean())
    df["dow"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    
    # Drop warm-up rows (first 28 days for each series that lack rolling windows)
    features_df = df.dropna().copy()
    print(f"Features created: {features_df.shape[0]} valid rows across 6 feature dimensions.")
    return features_df

if __name__ == "__main__":
    sales, inventory, deliveries = load_raw_data()
    clean_daily = clean_sales_data(sales)
    featured = add_time_features(clean_daily)
    featured.to_parquet("data/features.parquet", index=False)
    print("Saved features to data/features.parquet successfully.")
