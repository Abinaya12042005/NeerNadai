"""
generate_sample_data.py
------------------------
Idha yean venum: Kaggle-la irundhu real dataset download pannaadha varaikkum,
namma app work aaganum-nu ready sample data create panra script idhu.

REAL DATASET (mandatory for final submission):
Kaggle -> "Chennai Water Management" by sudalairajkumar
https://www.kaggle.com/datasets/sudalairajkumar/chennai-water-management
Files: chennai_reservoir_levels.csv, chennai_reservoir_rainfall.csv
(Real data from Chennai Metropolitan Water Supply & Sewerage Board)

Idhu 4 main reservoirs (=our "areas") oda daily water level (mcft) kudukkum:
POONDI, CHOLAVARAM, REDHILLS, CHEMBARAMBAKKAM

Ivanga naanga 4 "zones" of Chennai-nu treat panrom, so it fits the
"area-wise water wastage monitor" idea perfectly.

Run this ONCE to create sample data so you can test the site today itself.
Later, replace data/chennai_reservoir_levels.csv and
data/chennai_reservoir_rainfall.csv with the REAL Kaggle files
(same column names) - the app code doesn't need to change at all.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reproducible random data (so results don't jump around every run)
np.random.seed(42)

AREAS = ["POONDI", "CHOLAVARAM", "REDHILLS", "CHEMBARAMBAKKAM"]
DAYS = 365 * 2  # 2 years of daily data

start_date = datetime.today() - timedelta(days=DAYS)
dates = [start_date + timedelta(days=i) for i in range(DAYS)]

# --- 1. Reservoir levels (mcft = million cubic feet) ---
level_rows = []
base_capacity = {"POONDI": 3231, "CHOLAVARAM": 1081, "REDHILLS": 3300, "CHEMBARAMBAKKAM": 3645}

for area in AREAS:
    level = base_capacity[area] * 0.6  # start at 60% capacity
    for d in dates:
        # seasonal rainfall bump (monsoon = Oct-Dec in Chennai) + random daily draw-down
        month = d.month
        seasonal = 15 if month in (10, 11, 12) else -3
        level += seasonal + np.random.normal(0, 5)
        level = max(0, min(level, base_capacity[area]))  # clamp between 0 and full capacity
        level_rows.append({"Date": d.strftime("%d-%m-%Y"), "Area": area, "Level_mcft": round(level, 2)})

levels_df = pd.DataFrame(level_rows)
levels_df.to_csv("data/chennai_reservoir_levels.csv", index=False)

# --- 2. Rainfall (mm) per area ---
rain_rows = []
for area in AREAS:
    for d in dates:
        month = d.month
        base_rain = 25 if month in (10, 11, 12) else 2
        rain = max(0, np.random.exponential(base_rain))
        rain_rows.append({"Date": d.strftime("%d-%m-%Y"), "Area": area, "Rainfall_mm": round(rain, 2)})

rain_df = pd.DataFrame(rain_rows)
rain_df.to_csv("data/chennai_reservoir_rainfall.csv", index=False)

# --- 3. Derived: household/zone consumption + wastage estimate ---
# We estimate "wastage" as consumption above the recommended 135 litres/person/day
# (this is the Govt of India CPHEEO norm for urban water supply)
NORM_LPCD = 135
rows = []
for area in AREAS:
    population_share = np.random.randint(150000, 500000)  # approx people served
    for d in dates:
        # daily supply per person, with some areas over/under using
        actual_lpcd = NORM_LPCD + np.random.normal(10, 20)
        actual_lpcd = max(50, actual_lpcd)
        wastage_lpcd = max(0, actual_lpcd - NORM_LPCD)
        rows.append({
            "Date": d.strftime("%d-%m-%Y"),
            "Area": area,
            "Population_Served": population_share,
            "Actual_LPCD": round(actual_lpcd, 1),
            "Norm_LPCD": NORM_LPCD,
            "Wastage_LPCD": round(wastage_lpcd, 1),
        })

consumption_df = pd.DataFrame(rows)
consumption_df.to_csv("data/area_wise_consumption.csv", index=False)

print("Sample data created:")
print(" - data/chennai_reservoir_levels.csv   ", levels_df.shape)
print(" - data/chennai_reservoir_rainfall.csv ", rain_df.shape)
print(" - data/area_wise_consumption.csv      ", consumption_df.shape)
print("\nReplace the first two files with the REAL Kaggle CSVs before final submission.")
