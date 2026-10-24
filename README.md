# Logistics Data Analytics: Multi-Echelon Fulfillment Optimization

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License-MIT](https://img.shields.io/badge/License-Academic%20Internship-green.svg)
![Status-Complete](https://img.shields.io/badge/Status-Complete-success.svg)
![Dashboard](https://img.shields.io/badge/Dashboard-Interactive%20HTML%20%2B%20PNG-blueviolet.svg)

An end-to-end data analytics and machine learning solution for regional e-commerce fulfillment and last-mile distribution. Developed for an academic capstone/internship project by a B.E. student in Artificial Intelligence and Machine Learning at Acharya Institute of Technology, Bengaluru.

---

## 1. Executive Summary & Results

The project evaluates 24 months of multi-echelon supply chain operations (2024–2025; 219,300 facility-SKU-day observations) across 3 regional distribution hubs in Bengaluru (Peenya, Electronic City, and Whitefield) and 100 active SKUs.

### Key Performance Indicator (KPI) Scorecard

| KPI Metric | Mathematical Formula | Baseline Benchmark | Target Proposal | Achieved Result | Evaluation Status |
|---|---|---|---|---|---|
| **Demand Forecast Error (WAPE)** | $\frac{\sum \|y - \hat{y}\|}{\sum y}$ | 20.96% (7-day MA) | 10–15% relative improvement | **17.14% (18.21% relative reduction)** | **Met Target** |
| **Stockout Rate** | $\frac{\text{Unfulfilled Units}}{\text{Total Demand}}$ | 0.11% | 30% relative reduction | **0.07% (34.2% reduction [ASSUMPTION])** | **Met Target** |
| **Inventory Turnover Ratio** | $\frac{\text{Annualized COGS}}{\text{Average Total Inventory}}$ | 41.49x / year | Increase vs. baseline | **50.21x / year (+21% velocity)** | **Met Target** |
| **Warehouse Space Utilization** | $\frac{\text{Occupied Slots}}{\text{Total Available Slots}}$ | 37.5% | Shift from slow to fast SKUs | **82.5% (active fast-turn velocity)** | **Met Target** |
| **Route Distance per Stop** | $\frac{\text{Route Distance (km)}}{\text{Number of Stops}}$ | 12.45 km/stop | 10% reduction on sample days | **4.32 km/stop (65.3% reduction)** | **Exceeded Target** |

---

## 2. Project Architecture & Directory Layout

```
Logistics-data-analysis-week1/
├── data/
│   ├── sales.csv                     # Raw sales orders (200,155 records)
│   ├── inventory.csv                 # Daily stock snapshots (219,300 records)
│   ├── deliveries.csv                # Dispatch logs & coordinates (1,888 stops)
│   ├── features.parquet              # Leakage-free lag & rolling feature matrix
│   └── data_dictionary.md            # Data dictionary and variable definitions
├── src/
│   ├── generate_data.py              # Synthetic generation with seasonality & trends
│   ├── clean_and_engineer.py         # MultiIndex zero-fill & lag/rolling feature pipeline
│   ├── forecasting.py                # GBR, baseline 7-day MA, ARIMA, multi-window backtesting
│   ├── segmentation.py               # K-Means clustering, silhouette & temporal stability
│   ├── anomaly_detection.py          # Isolation Forest & z-score anomaly triage
│   ├── route_optimization.py         # Haversine, Nearest Neighbor, 2-Opt local search
│   ├── generate_docx_report.py       # Automated DOCX academic report compiler
│   └── logistics_analysis.py         # Master pipeline orchestrator
├── outputs/
│   ├── forecast_comparison.png       # 8-week holdout forecast visualization
│   ├── inventory_clusters.png        # SKU demand vs. volatility scatter plot
│   ├── route_optimization.png        # Before/after route untangling visualization
│   ├── kpi_summary.csv               # Summary table of 5 core logistics KPIs
│   ├── model_comparison.csv          # Comparative evaluation (MA vs GBR vs ARIMA)
│   ├── sku_segments.csv              # Granular SKU policy allocations
│   ├── anomaly_review_sample.csv     # 20-record clinical inspection sample
│   ├── route_optimization_comparison.csv # Baseline vs NN vs 2-Opt route distances
│   └── results_summary.md            # Comprehensive Markdown results report
├── powerbi/
│   ├── dashboard.html                # Interactive 5-page analytics dashboard (Chart.js)
│   ├── page1_executive_summary.png   # KPI cards, radar chart, utilization gauge
│   ├── page2_demand_forecast.png     # WAPE comparison, Top-10 SKUs, monthly revenue
│   ├── page3_inventory_health.png    # Segment donut, stock trend, SKU scatter plot
│   ├── page4_route_optimization.png  # Route comparison bars, progress bars, delivery map
│   └── page5_anomaly_detection.png   # Anomaly donut, warehouse stacked bar, Z-score chart
├── report/
│   ├── Strategic_Planning_Logistics_Report.md   # Publication-grade academic report
│   └── Strategic_Planning_Logistics_Report.docx # Formatted Word deliverable
├── presentation_outline.md           # 8-Slide capstone presentation deck outline
├── references.md                     # Verified academic & technical citations
├── Logistics_Project_Brief.md        # Original project specification brief
└── requirements.txt                  # Python dependencies
```

---

## 3. Installation & Environment Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### Setup Instructions

```bash
# Clone the repository
git clone https://github.com/pranjal/Logistics-data-analysis-week1.git
cd Logistics-data-analysis-week1

# Install required dependencies
pip install -r requirements.txt
```

---

## 4. Execution Sequence (Run Order)

The analytics workflow can be executed in sequence or automatically through the master pipeline orchestrator:

### Option A: Complete Automated Execution (Recommended)
```bash
python src/logistics_analysis.py
```
This executes the entire end-to-end pipeline:
1. Ingests raw data from `data/`
2. Cleans duplicates, filters negative values, and creates full Cartesian MultiIndex grid zero-fill
3. Generates leakage-free lag and rolling features
4. Fits baseline, Gradient Boosting Regressor, and ARIMA models
5. Conducts 2-window backtesting stability verification
6. Runs K-Means segmentation with silhouette evaluation and temporal stability testing
7. Executes Isolation Forest anomaly detection
8. Solves last-mile route sequencing using 2-Opt heuristics
9. Exports all summary tables and high-resolution charts to `outputs/`

### Option B: Step-by-Step Module Execution
1. **Data Generation:**
   ```bash
   python src/generate_data.py
   ```
2. **Data Cleaning & Feature Engineering:**
   ```bash
   python src/clean_and_engineer.py
   ```
3. **Demand Forecasting & Backtesting:**
   ```bash
   python src/forecasting.py
   ```
4. **Inventory Segmentation:**
   ```bash
   python src/segmentation.py
   ```
5. **Anomaly Detection:**
   ```bash
   python src/anomaly_detection.py
   ```
6. **Route Optimization:**
   ```bash
   python src/route_optimization.py
   ```
7. **Generate Word Document Report:**
   ```bash
   python src/generate_docx_report.py
   ```

---

## 5. Algorithmic Highlights

### Multi-Horizon Demand Forecasting
- **Leakage-Free Features:** Uses `shift(1)` before computing 7-day and 28-day rolling averages so target day demand is never exposed.
- **Model:** Gradient Boosting Regressor with 100 estimators, max depth 5, learning rate 0.08.
- **Backtesting Stability:** Evaluated on two independent 8-week test partitions (Weeks 97–104 and Weeks 89–96), maintaining 17.14% and 17.12% WAPE respectively.

### Inventory Clustering & Policy Allocation
- **Features:** Mean daily demand and demand coefficient of variation ($CV = \sigma / \mu$).
- **Diagnostics:** Peak silhouette score of 0.6530 at $k=4$.
- **Temporal Stability:** Adjusted Rand Index (ARI) of **1.000** between 2024 and 2025 allocations.

### Spatial Last-Mile Route Optimization
- **Problem Formulation:** Traveling Salesperson Problem (TSP) over daily dispatch waypoints.
- **Methodology:** Haversine distance matrix $\rightarrow$ Nearest Neighbor constructive tour $\rightarrow$ 2-Opt local search edge-exchange untangling.
- **Performance:** Reduced distance from 311.33 km down to 108.08 km (65.3% reduction).

---

## 6. Interactive Analytics Dashboard

A fully interactive, multi-page analytics dashboard was built in HTML + Chart.js to visualise all project results. It is available in two formats:

| Format | Location | Description |
|---|---|---|
| **Static PNGs (×5)** | [`powerbi/`](powerbi/) | One high-resolution PNG per dashboard page, ready for report/presentation embedding |

### Dashboard Pages

| Page | File | Charts & Visuals |
|---|---|---|
| **1 — Executive Summary** | `page1_executive_summary.png` | 5 KPI cards · KPI summary table · Achievement radar · Utilization gauge |
| **2 — Demand & Forecasting** | `page2_demand_forecast.png` | WAPE model comparison · Top-10 SKUs · Monthly revenue by warehouse · Day-of-week demand · Forecast bias |
| **3 — Inventory Health** | `page3_inventory_health.png` | Segment donut (AX/CZ) · Stock-on-hand trend · SKU scatter (demand vs CV) · Policy table |
| **4 — Route Optimization** | `page4_route_optimization.png` | Route distance bar · Distance/stop bar · % improvement bars · Bangalore delivery map |
| **5 — Anomaly Detection** | `page5_anomaly_detection.png` | Event-type donut · Warehouse stacked bar · Z-score column · Flagged event detail table |

### Dashboard Preview

> Open [`powerbi/dashboard.html`](powerbi/dashboard.html) in any modern browser (Chrome, Edge, Firefox) for the full interactive experience. No server or installation required.

---

## 7. Academic References

All algorithms, metrics, and models are grounded in peer-reviewed literature. See [`references.md`](references.md) for full details:
- **Hyndman & Koehler (2006):** Forecast accuracy metrics (WAPE vs. MAPE under intermittent demand).
- **Silver, Pyke, & Peterson (1998):** Multi-echelon inventory systems and ABC/XYZ classification.
- **Liu, Ting, & Zhou (2008):** Isolation Forest for data quality surveillance.
- **Croes (1958) & Toth & Vigo (2014):** 2-Opt local search heuristic and Vehicle Routing Problems.

---

## 8. Project Deliverables Checklist

| # | Deliverable | File | Status |
|---|---|---|---|
| 1 | Strategy & Planning Report (Markdown) | `report/Strategic_Planning_Logistics_Report.md` | ✅ Complete |
| 2 | Strategy & Planning Report (Word) | `report/Strategic_Planning_Logistics_Report.docx` | ✅ Complete |
| 3 | Code Repository with README | `README.md` + `src/` | ✅ Complete |
| 4 | KPI Results Summary Table | `outputs/kpi_summary.csv` | ✅ Complete |
| 5 | Model Comparison Table | `outputs/model_comparison.csv` | ✅ Complete |
| 6 | SKU Segments & Policy Map | `outputs/sku_segments.csv` | ✅ Complete |
| 7 | Anomaly Review Sample | `outputs/anomaly_review_sample.csv` | ✅ Complete |
| 8 | Route Optimization Comparison | `outputs/route_optimization_comparison.csv` | ✅ Complete |
| 9 | Academic References | `references.md` | ✅ Complete |
| 10 | Presentation Outline (8 slides) | `presentation_outline.md` | ✅ Complete |
| 11 | **Dashboard PNGs (×5 pages)** | `powerbi/page1_*.png … page5_*.png` | ✅ Complete |
