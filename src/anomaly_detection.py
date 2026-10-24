"""
Phase 5: Anomaly Detection via Isolation Forest
Implements Section 7.7:
- Computes within-SKU z-scores for demand variation
- Fits an Isolation Forest (contamination=0.01) on (units_sold, z_within_sku)
- Extracts flagged records and generates an inspection sample table (20 records)
  categorized into operational event types (demand surges, promo spikes, abnormal drops).
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_demand_anomalies(daily_df, contamination=0.01, random_state=42):
    print("\n--- Section 7.7: Demand Anomaly Detection ---")
    df = daily_df.copy()
    
    # Calculate within-SKU z-score
    print("Calculating within-SKU demand z-scores...")
    df["z_within_sku"] = df.groupby("sku_id")["units_sold"].transform(
        lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0.0
    )
    
    iso = IsolationForest(contamination=contamination, random_state=random_state)
    df["anomaly"] = iso.fit_predict(df[["units_sold", "z_within_sku"]])
    
    flagged = df[df["anomaly"] == -1].copy()
    flag_rate = len(flagged) / len(df) * 100
    print(f"Total evaluated records: {len(df):,}")
    print(f"Flagged anomaly records: {len(flagged):,} ({flag_rate:.2f}%)")
    
    # Classify anomalies into operational archetypes for manual review
    def categorize_event(row):
        if row["z_within_sku"] > 3.0:
            return "Extreme Demand Surge / Promotional Spike"
        elif row["z_within_sku"] > 2.0:
            return "Moderate Demand Spike"
        elif row["units_sold"] == 0 and row["z_within_sku"] < -1.5:
            return "Severe Stockout / Unrecorded Sales Gap"
        else:
            return "Distribution Tail Outlier"
            
    flagged["event_type"] = flagged.apply(categorize_event, axis=1)
    
    # Draw representative 20-sample inspection set
    sample_review = flagged.sample(n=min(20, len(flagged)), random_state=random_state)
    sample_display = sample_review[[
        "date", "sku_id", "warehouse_id", "units_sold", "z_within_sku", "event_type"
    ]].sort_values("date")
    
    print("\nSample Anomaly Review Table (20 Records):")
    print(sample_display.to_string(index=False))
    
    # Summary of event types
    event_summary = flagged["event_type"].value_counts().reset_index()
    event_summary.columns = ["Event Type", "Count"]
    print("\nAnomaly Breakdown by Archetype:")
    print(event_summary.to_string(index=False))
    
    return flagged, sample_display, {
        "total_records": len(df),
        "flagged_count": len(flagged),
        "contamination": contamination,
        "sample_review": sample_display
    }

if __name__ == "__main__":
    from clean_and_engineer import load_raw_data, clean_sales_data
    sales, _, _ = load_raw_data()
    clean_daily = clean_sales_data(sales)
    flagged, sample_rev, metrics = detect_demand_anomalies(clean_daily)
    sample_rev.to_csv("outputs/anomaly_review_sample.csv", index=False)
