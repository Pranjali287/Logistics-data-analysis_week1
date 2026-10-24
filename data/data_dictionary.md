# Logistics Data Dictionary

This dataset simulates a regional multi-echelon e-commerce fulfillment operation in Bengaluru (Bangalore), Karnataka, India, serving metropolitan consumers over a 24-month horizon (January 1, 2024 to December 31, 2025).

---

## 1. sales.csv
Records daily product transactions across fulfillment centers.

| Field Name | Data Type | Key / Constraint | Description | Example |
|---|---|---|---|---|
| `date` | Date (`YYYY-MM-DD`) | Temporal Index | Date of retail fulfillment / sale | `2024-05-15` |
| `sku_id` | String | Foreign Key | Standardized SKU identifier (`SKU_001` to `SKU_100`) | `SKU_042` |
| `warehouse_id` | String | Foreign Key | Fulfilling regional distribution center | `WH_BLR_NORTH` |
| `units_sold` | Integer | $\ge 0$ | Number of consumer units dispatched | `28` |
| `unit_price` | Float | $> 0$ (INR) | Final selling price per unit in Indian Rupees | `499.00` |

---

## 2. inventory.csv
Daily end-of-day stock positions, replenishment tracking, and unit valuations.

| Field Name | Data Type | Key / Constraint | Description | Example |
|---|---|---|---|---|
| `date` | Date (`YYYY-MM-DD`) | Temporal Index | Daily inventory snapshot timestamp | `2024-05-15` |
| `sku_id` | String | Foreign Key | Standardized SKU identifier | `SKU_042` |
| `warehouse_id` | String | Foreign Key | Warehouse facility storing the physical inventory | `WH_BLR_NORTH` |
| `stock_on_hand` | Integer | $\ge 0$ | Physical units available in storage at close of day | `142` |
| `unit_cost` | Float | $> 0$ (INR) | Landed inventory procurement cost per unit | `295.50` |

---

## 3. deliveries.csv
Last-mile delivery dispatch logs from distribution depots to consumer drop locations across Bengaluru.

| Field Name | Data Type | Key / Constraint | Description | Example |
|---|---|---|---|---|
| `delivery_id` | String | Primary Key | Unique delivery run/consignment identifier | `DEL_20251015_001` |
| `date` | Date (`YYYY-MM-DD`) | Temporal Filter | Day of dispatch | `2025-10-15` |
| `warehouse_id` | String | Origin Depot | Fulfillment center originating the vehicle | `WH_BLR_SOUTH` |
| `stop_lat` | Float | $-90.0 \le \phi \le 90.0$ | Latitude coordinate of delivery waypoint | `12.9250` |
| `stop_lon` | Float | $-180.0 \le \lambda \le 180.0$ | Longitude coordinate of delivery waypoint | `77.6850` |
| `distance_km` | Float | $> 0$ | Historic dispatcher-assigned route distance (km) | `4.8` |

---

## Warehouse Facilities (Bengaluru Metropolitan Region)
1. **WH_BLR_NORTH (Peenya Industrial Area)**: Latitude `13.0285`, Longitude `77.5197`
2. **WH_BLR_SOUTH (Electronic City Phase 1)**: Latitude `12.8452`, Longitude `77.6602`
3. **WH_BLR_EAST (Whitefield Industrial Zone)**: Latitude `12.9698`, Longitude `77.7499`

---

## Assumptions & Data Synthesis Notes [ASSUMPTION]
- Historical timeline: 730 days (24 continuous calendar months).
- 100 representative SKUs segmented realistically into Fast-moving consumer goods (ABC Pareto distribution: Top 20% generate ~70% volume; remaining 80% moderate-to-slow volume).
- Seasonality: Weekly retail cycle (Saturday/Sunday peaks ~25-35%), Q4 festival shopping peak (Diwali / Big Billion Days surges ~40-60%), random Poisson noise, and deliberate promo anomalies for anomaly detection validation.
- Inventory reorder policy: (s, S) periodic review reorder with 3-day lead times and stockout occurrences during extreme surges.
