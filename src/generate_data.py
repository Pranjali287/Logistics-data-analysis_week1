"""
Logistics Data Generator
Generates synthetic sales, inventory, and delivery datasets adhering to Section 5.1 and 5.2.
Simulates a regional fulfillment network in Bengaluru with 3 warehouses, 100 SKUs, over 24 months.
Includes seasonality, trends, promotions, stockouts, and last-mile dispatch routing.
"""

import os
import math
import numpy as np
import pandas as pd

def generate_logistics_data(output_dir="data", seed=42):
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    
    print("[1/3] Generating sales.csv...")
    warehouses = ["WH_BLR_NORTH", "WH_BLR_SOUTH", "WH_BLR_EAST"]
    n_skus = 100
    skus = [f"SKU_{i+1:03d}" for i in range(n_skus)]
    
    # 24 months date range: 2024-01-01 to 2025-12-31 (730 days)
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    n_days = len(dates)
    
    # SKU Profiles: ABC distribution
    # Top 20 SKUs: High volume (A)
    # Next 30 SKUs: Medium volume (B)
    # Remaining 50 SKUs: Low volume / intermittent (C)
    sku_base_demand = {}
    sku_prices = {}
    sku_costs = {}
    
    for i, sku in enumerate(skus):
        if i < 20: # Class A
            base = np.random.uniform(25, 60)
            price = np.random.uniform(300, 1200)
        elif i < 50: # Class B
            base = np.random.uniform(8, 22)
            price = np.random.uniform(150, 800)
        else: # Class C
            base = np.random.uniform(0.5, 6)
            price = np.random.uniform(80, 2500)
        
        # Cost is ~60-75% of price
        margin_pct = np.random.uniform(0.20, 0.35)
        cost = price * (1 - margin_pct)
        
        sku_base_demand[sku] = base
        sku_prices[sku] = round(price, 2)
        sku_costs[sku] = round(cost, 2)

    # Warehouse volume weighting
    wh_weights = {"WH_BLR_NORTH": 1.15, "WH_BLR_SOUTH": 1.05, "WH_BLR_EAST": 0.80}

    sales_records = []
    
    # Day-of-week multipliers (Mon=0 -> Sun=6)
    dow_multipliers = [0.88, 0.92, 0.95, 1.00, 1.12, 1.25, 1.18]
    
    for day_idx, d in enumerate(dates):
        day_of_year = d.dayofyear
        dow = d.dayofweek
        
        # Yearly seasonality: surge around festive quarter Q4 (Diwali / Big Billion Days around Oct-Nov)
        # Peak around day 290-320
        annual_factor = 1.0 + 0.35 * np.exp(-((day_of_year - 305) ** 2) / (2 * (30 ** 2)))
        # Trend factor (10% annual growth)
        trend_factor = 1.0 + 0.10 * (day_idx / 365.25)
        
        dow_factor = dow_multipliers[dow]
        
        for wh in warehouses:
            wh_factor = wh_weights[wh]
            
            for sku in skus:
                base = sku_base_demand[sku]
                expected = base * wh_factor * dow_factor * annual_factor * trend_factor
                
                # Occasional promotional flash sales (anomalies)
                if np.random.rand() < 0.003: # 0.3% chance of surge
                    expected *= np.random.uniform(2.5, 4.5)
                
                # Poisson / Neg-binomial demand sampling
                units = np.random.poisson(expected)
                
                # For slow moving C items, many zero sales days
                if sku_base_demand[sku] < 3 and np.random.rand() < 0.35:
                    units = 0
                
                # Add to sales records (occasionally some records are zero; keep valid non-negative sales)
                if units > 0 or np.random.rand() < 0.15: # retain realistic transaction sparsity
                    sales_records.append({
                        "date": d.strftime("%Y-%m-%d"),
                        "sku_id": sku,
                        "warehouse_id": wh,
                        "units_sold": int(units),
                        "unit_price": sku_prices[sku]
                    })
    
    # Introduce a few realistic duplicates / negative entries to simulate raw real-world dirty data
    # that our clean_and_engineer pipeline will catch and resolve
    dirty_sales = pd.DataFrame(sales_records)
    # Add 5 duplicates
    duplicates = dirty_sales.sample(5, random_state=42)
    # Add 3 return records (negative units)
    negatives = dirty_sales.sample(3, random_state=42).copy()
    negatives["units_sold"] = -np.random.randint(1, 5, size=len(negatives))
    
    sales_df = pd.concat([dirty_sales, duplicates, negatives], ignore_index=True)
    sales_path = os.path.join(output_dir, "sales.csv")
    sales_df.to_csv(sales_path, index=False)
    print(f"   -> sales.csv created: {sales_df.shape[0]} rows, {sales_df.shape[1]} columns")

    print("[2/3] Generating inventory.csv...")
    # Simulate daily inventory with (s, S) replenishment policy
    inv_records = []
    
    # Pre-index sales for rapid lookup
    clean_sales_lookup = dirty_sales.groupby(["date", "sku_id", "warehouse_id"])["units_sold"].sum().to_dict()
    
    # Initial inventory state per (sku, wh)
    current_stock = {}
    reorder_point = {}
    target_stock = {}
    pending_orders = {} # list of (arrival_date, qty)
    
    for wh in warehouses:
        for sku in skus:
            key = (sku, wh)
            avg_d = sku_base_demand[sku] * wh_weights[wh]
            reorder_point[key] = max(5, int(avg_d * 7))     # 7 days lead time safety buffer
            target_stock[key] = max(20, int(avg_d * 21))    # 21 days cycle stock target
            current_stock[key] = target_stock[key]
            pending_orders[key] = []

    for d in dates:
        d_str = d.strftime("%Y-%m-%d")
        
        for wh in warehouses:
            for sku in skus:
                key = (sku, wh)
                
                # Check arrived replenishment shipments (Lead time = 3 days)
                arrived_qty = sum(qty for arr_date, qty in pending_orders[key] if arr_date == d_str)
                current_stock[key] += arrived_qty
                # Filter out past arrived orders
                pending_orders[key] = [(arr_date, qty) for arr_date, qty in pending_orders[key] if arr_date > d_str]
                
                # Realized sales depletion
                sold = clean_sales_lookup.get((d_str, sku, wh), 0)
                
                # Check stockout
                if current_stock[key] >= sold:
                    current_stock[key] -= sold
                else:
                    # Stockout occurred! All stock depleted
                    current_stock[key] = 0
                
                # Check reorder condition
                effective_inventory = current_stock[key] + sum(qty for _, qty in pending_orders[key])
                if effective_inventory <= reorder_point[key]:
                    order_qty = target_stock[key] - effective_inventory
                    # Lead time: 3 days
                    arr_date = (d + pd.Timedelta(days=3)).strftime("%Y-%m-%d")
                    pending_orders[key].append((arr_date, order_qty))
                
                inv_records.append({
                    "date": d_str,
                    "sku_id": sku,
                    "warehouse_id": wh,
                    "stock_on_hand": int(current_stock[key]),
                    "unit_cost": sku_costs[sku]
                })

    inv_df = pd.DataFrame(inv_records)
    inv_path = os.path.join(output_dir, "inventory.csv")
    inv_df.to_csv(inv_path, index=False)
    print(f"   -> inventory.csv created: {inv_df.shape[0]} rows, {inv_df.shape[1]} columns")

    print("[3/3] Generating deliveries.csv...")
    # Warehouse coordinates (Bangalore)
    wh_coords = {
        "WH_BLR_NORTH": (13.0285, 77.5197),  # Peenya
        "WH_BLR_SOUTH": (12.8452, 77.6602),  # Electronic City
        "WH_BLR_EAST":  (12.9698, 77.7499)   # Whitefield
    }
    
    delivery_records = []
    del_counter = 1
    
    # Generate delivery dispatches for sample operational days
    # (Focusing across several sample dates including peak and off-peak days)
    sample_dates = pd.date_range("2025-10-01", "2025-10-31", freq="D")
    
    def haversine_dist(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        return 2 * 6371 * math.asin(math.sqrt(a))
    
    for d in sample_dates:
        d_str = d.strftime("%Y-%m-%d")
        for wh, (depot_lat, depot_lon) in wh_coords.items():
            # 15 to 25 delivery stops per warehouse per day
            n_stops = np.random.randint(15, 26)
            
            # Stops clustered within ~12 km radius of warehouse
            lats = depot_lat + np.random.normal(0, 0.045, n_stops)
            lons = depot_lon + np.random.normal(0, 0.045, n_stops)
            
            # Dispatcher baseline sequence (often suboptimal/heuristic order with zigzagging)
            # Simulate historical dispatcher sequence distance
            prev_lat, prev_lon = depot_lat, depot_lon
            for stop_idx in range(n_stops):
                stop_lat, stop_lon = lats[stop_idx], lons[stop_idx]
                leg_dist = haversine_dist(prev_lat, prev_lon, stop_lat, stop_lon)
                # Dispatcher road detour inefficiency factor (~1.25 to 1.45x haversine)
                actual_recorded_km = leg_dist * np.random.uniform(1.25, 1.45)
                
                delivery_records.append({
                    "delivery_id": f"DEL_{d.strftime('%Y%m%d')}_{del_counter:04d}",
                    "date": d_str,
                    "warehouse_id": wh,
                    "stop_lat": round(float(stop_lat), 5),
                    "stop_lon": round(float(stop_lon), 5),
                    "distance_km": round(float(actual_recorded_km), 2)
                })
                del_counter += 1
                prev_lat, prev_lon = stop_lat, stop_lon
                
    del_df = pd.DataFrame(delivery_records)
    del_path = os.path.join(output_dir, "deliveries.csv")
    del_df.to_csv(del_path, index=False)
    print(f"   -> deliveries.csv created: {del_df.shape[0]} rows, {del_df.shape[1]} columns")
    print("All datasets successfully generated!")

if __name__ == "__main__":
    generate_logistics_data()
