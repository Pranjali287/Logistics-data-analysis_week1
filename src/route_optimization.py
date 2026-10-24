"""
Phase 5 / Section 7.8: Route Optimization Heuristics
Implements:
1. Haversine spherical distance calculation
2. Baseline dispatcher route distance computation
3. Nearest Neighbor construction heuristic
4. 2-Opt local search edge-exchange improvement heuristic
5. Comparative evaluation and route kilometer savings summary
"""

import math
import numpy as np
import pandas as pd

def haversine_km(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * 6371 * math.asin(math.sqrt(h))

def route_length(route, dist_fn):
    return sum(dist_fn(route[i], route[i + 1]) for i in range(len(route) - 1))

def nearest_neighbor(depot, stops, dist_fn):
    route = [depot]
    remaining = set(stops)
    while remaining:
        nxt = min(remaining, key=lambda s: dist_fn(route[-1], s))
        route.append(nxt)
        remaining.remove(nxt)
    route.append(depot) # Return to depot
    return route

def two_opt(route, dist_fn):
    best_route = list(route)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                a, b = best_route[i - 1], best_route[i]
                c, d = best_route[j], best_route[j + 1]
                # Check if reversing the sub-tour [i, j] reduces distance
                if dist_fn(a, c) + dist_fn(b, d) < dist_fn(a, b) + dist_fn(c, d) - 1e-9:
                    best_route[i:j + 1] = reversed(best_route[i:j + 1])
                    improved = True
    return best_route

def optimize_sample_day_routes(deliveries_df, sample_date="2025-10-15", sample_wh="WH_BLR_NORTH"):
    print(f"\n--- Section 7.8: Route Optimization for {sample_wh} on {sample_date} ---")
    
    # Depot coordinates
    wh_coords = {
        "WH_BLR_NORTH": (13.0285, 77.5197),  # Peenya
        "WH_BLR_SOUTH": (12.8452, 77.6602),  # Electronic City
        "WH_BLR_EAST":  (12.9698, 77.7499)   # Whitefield
    }
    depot = wh_coords[sample_wh]
    
    # Filter day and warehouse stops
    sub_df = deliveries_df[(deliveries_df["date"] == sample_date) & 
                           (deliveries_df["warehouse_id"] == sample_wh)].copy()
    
    if len(sub_df) == 0:
        # Fallback to any valid date in dataset
        sample_date = deliveries_df["date"].iloc[0]
        sample_wh = deliveries_df["warehouse_id"].iloc[0]
        depot = wh_coords[sample_wh]
        sub_df = deliveries_df[(deliveries_df["date"] == sample_date) & 
                               (deliveries_df["warehouse_id"] == sample_wh)].copy()
        
    stops = [tuple(x) for x in sub_df[["stop_lat", "stop_lon"]].values]
    num_stops = len(stops)
    
    # 1. Dispatcher Baseline Route
    # Dispatcher historic logged route: starts at depot, visits stops in recorded sequence, returns to depot
    dispatcher_route = [depot] + stops + [depot]
    disp_haversine_km = route_length(dispatcher_route, haversine_km)
    recorded_actual_road_km = float(sub_df["distance_km"].sum())
    
    # 2. Nearest Neighbor Heuristic
    nn_route = nearest_neighbor(depot, stops, haversine_km)
    nn_haversine_km = route_length(nn_route, haversine_km)
    
    # 3. 2-Opt Local Search Heuristic
    two_opt_route = two_opt(nn_route, haversine_km)
    two_opt_haversine_km = route_length(two_opt_route, haversine_km)
    
    nn_improvement = (disp_haversine_km - nn_haversine_km) / disp_haversine_km * 100.0
    two_opt_improvement = (disp_haversine_km - two_opt_haversine_km) / disp_haversine_km * 100.0
    
    # Road detour factor: typical Bangalore road circuity factor is ~1.32x haversine
    estimated_optimized_road_km = two_opt_haversine_km * 1.32
    road_savings_km = recorded_actual_road_km - estimated_optimized_road_km
    road_savings_pct = (road_savings_km / recorded_actual_road_km) * 100.0
    
    print(f"Stops serviced: {num_stops}")
    print(f"Dispatcher Sequence (Haversine): {disp_haversine_km:.2f} km (Recorded Road: {recorded_actual_road_km:.2f} km)")
    print(f"Nearest Neighbor Heuristic:      {nn_haversine_km:.2f} km ({nn_improvement:.1f}% reduction)")
    print(f"2-Opt Edge-Exchange Optimized:   {two_opt_haversine_km:.2f} km ({two_opt_improvement:.1f}% reduction vs Dispatcher)")
    print(f"Estimated Realized Road Savings:  {road_savings_km:.2f} km saved ({road_savings_pct:.1f}% reduction)")
    
    comparison_table = pd.DataFrame([
        {"Method": "Historic Dispatcher Baseline", "Haversine Distance (km)": round(disp_haversine_km, 2), "Distance per Stop (km)": round(disp_haversine_km / num_stops, 2), "Improvement vs Baseline": "0.0% (Baseline)"},
        {"Method": "Nearest Neighbor Heuristic", "Haversine Distance (km)": round(nn_haversine_km, 2), "Distance per Stop (km)": round(nn_haversine_km / num_stops, 2), "Improvement vs Baseline": f"-{nn_improvement:.1f}%"},
        {"Method": "2-Opt Edge-Exchange Optimized", "Haversine Distance (km)": round(two_opt_haversine_km, 2), "Distance per Stop (km)": round(two_opt_haversine_km / num_stops, 2), "Improvement vs Baseline": f"-{two_opt_improvement:.1f}%"}
    ])
    
    return {
        "sample_date": sample_date,
        "warehouse_id": sample_wh,
        "num_stops": num_stops,
        "depot_coord": depot,
        "dispatcher_route": dispatcher_route,
        "two_opt_route": two_opt_route,
        "disp_km": disp_haversine_km,
        "two_opt_km": two_opt_haversine_km,
        "improvement_pct": two_opt_improvement,
        "comparison_table": comparison_table
    }

if __name__ == "__main__":
    del_df = pd.read_csv("data/deliveries.csv")
    res = optimize_sample_day_routes(del_df)
    res["comparison_table"].to_csv("outputs/route_optimization_comparison.csv", index=False)
