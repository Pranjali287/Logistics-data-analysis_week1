"""
Phase 5: Inventory Segmentation via K-Means and ABC/XYZ Analysis
Implements Section 7.6:
- Calculates SKU profiles (total_units, mean_daily, cv_demand)
- Evaluates optimal k using both Elbow inertia and Silhouette scores (k in 2..7)
- Interprets and labels business segments ("Fast & Steady", "Fast & Volatile", etc.)
- Assesses cluster stability across two time windows (2024 vs 2025) per Objective O2.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

def perform_sku_segmentation(daily_df):
    print("\n--- Section 7.6: SKU Clustering and Segmentation ---")
    
    sku_profile = (daily_df.groupby("sku_id")
                   .agg(
                       total_units=("units_sold", "sum"),
                       mean_daily=("units_sold", "mean"),
                       std_daily=("units_sold", "std")
                   )
                   .reset_index())
    
    sku_profile["cv_demand"] = sku_profile.apply(
        lambda r: (r["std_daily"] / r["mean_daily"]) if r["mean_daily"] > 0 else 0.0,
        axis=1
    )
    
    features_for_clustering = ["mean_daily", "cv_demand"]
    scaler = StandardScaler()
    X = scaler.fit_transform(sku_profile[features_for_clustering])
    
    # 1. Evaluate k from 2 to 7 with Silhouette score and Inertia
    silhouette_scores = {}
    inertias = {}
    
    for k in range(2, 8):
        km = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = km.fit_predict(X)
        score = silhouette_score(X, labels)
        silhouette_scores[k] = float(score)
        inertias[k] = float(km.inertia_)
        print(f" k={k}: Silhouette Score = {score:.4f}, Inertia = {km.inertia_:.2f}")
        
    best_k = max(silhouette_scores, key=silhouette_scores.get)
    # Often k=4 yields classic 2x2 ABC/XYZ mapping (Mean vs Volatility)
    selected_k = 4 if 4 in silhouette_scores and silhouette_scores[4] > 0.45 else best_k
    print(f"\nSelected k = {selected_k} (Optimal balance of silhouette score: {silhouette_scores[selected_k]:.4f} and 2x2 operational interpretability)")
    
    final_km = KMeans(n_clusters=selected_k, n_init=10, random_state=42)
    sku_profile["cluster"] = final_km.fit_predict(X)
    
    # Label clusters based on cluster centroids
    cluster_stats = sku_profile.groupby("cluster")[["mean_daily", "cv_demand", "total_units"]].mean()
    print("\nCluster Centroids:")
    print(cluster_stats)
    
    # Assign intuitive managerial names based on relative centroid thresholds
    overall_mean_daily = sku_profile["mean_daily"].median()
    overall_mean_cv = sku_profile["cv_demand"].median()
    
    label_map = {}
    policy_map = {}
    for cl_id, row in cluster_stats.iterrows():
        is_fast = row["mean_daily"] >= overall_mean_daily
        is_volatile = row["cv_demand"] >= overall_mean_cv
        
        if is_fast and not is_volatile:
            name = "Fast & Steady (AX)"
            policy = "Automated continuous review, lean safety stock, frequent replenishment"
        elif is_fast and is_volatile:
            name = "Fast & Volatile (AY)"
            policy = "Dynamic buffer sizing, close supplier collaboration, higher safety stock"
        elif not is_fast and not is_volatile:
            name = "Slow & Steady (CX)"
            policy = "Periodic batch review, min-max ordering, low holding priority"
        else:
            name = "Slow & Erratic (CZ)"
            policy = "Order-on-demand / drop-ship, central consolidation, prune long-tail"
            
        label_map[cl_id] = name
        policy_map[cl_id] = policy
        
    sku_profile["segment_name"] = sku_profile["cluster"].map(label_map)
    sku_profile["inventory_policy"] = sku_profile["cluster"].map(policy_map)
    
    print("\nSegment Distribution & Policy Mapping:")
    summary_table = sku_profile.groupby("segment_name").agg(
        sku_count=("sku_id", "count"),
        avg_daily_demand=("mean_daily", "mean"),
        avg_cv=("cv_demand", "mean"),
        total_volume=("total_units", "sum"),
        policy=("inventory_policy", "first")
    ).reset_index()
    print(summary_table.to_string(index=False))
    
    # --- Stability Verification Across Two 12-Month Windows (Objective O2) ---
    print("\n--- Stability Check: Year 2024 vs Year 2025 ---")
    daily_2024 = daily_df[daily_df["date"] < "2025-01-01"]
    daily_2025 = daily_df[daily_df["date"] >= "2025-01-01"]
    
    prof_2024 = daily_2024.groupby("sku_id").agg(
        mean_daily=("units_sold", "mean"),
        cv_demand=("units_sold", lambda s: s.std() / s.mean() if s.mean() > 0 else 0)
    ).reindex(sku_profile["sku_id"])
    
    prof_2025 = daily_2025.groupby("sku_id").agg(
        mean_daily=("units_sold", "mean"),
        cv_demand=("units_sold", lambda s: s.std() / s.mean() if s.mean() > 0 else 0)
    ).reindex(sku_profile["sku_id"])
    
    X_2024 = StandardScaler().fit_transform(prof_2024.fillna(0))
    X_2025 = StandardScaler().fit_transform(prof_2025.fillna(0))
    
    labels_2024 = KMeans(n_clusters=selected_k, n_init=10, random_state=42).fit_predict(X_2024)
    labels_2025 = KMeans(n_clusters=selected_k, n_init=10, random_state=42).fit_predict(X_2025)
    
    ari = adjusted_rand_score(labels_2024, labels_2025)
    print(f"Adjusted Rand Index between 2024 and 2025 clusters: {ari:.3f}")
    if ari > 0.60:
        print("  -> High temporal cluster stability confirmed across consecutive annual operating periods.")
    else:
        print("  -> Moderate cluster drift detected; quarterly re-clustering recommended.")
        
    return sku_profile, summary_table, {
        "selected_k": selected_k,
        "silhouette_scores": silhouette_scores,
        "inertias": inertias,
        "adjusted_rand_index": float(ari)
    }

if __name__ == "__main__":
    from clean_and_engineer import load_raw_data, clean_sales_data
    sales, _, _ = load_raw_data()
    clean_daily = clean_sales_data(sales)
    sku_profile, summary_table, metrics = perform_sku_segmentation(clean_daily)
    sku_profile.to_csv("outputs/sku_segments.csv", index=False)
