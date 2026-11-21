
# ================= 1. IMPORT LIBRARIES =================

import pandas as pd
import numpy as np


# ================= 2. LOAD CSV FILE =================

df = pd.read_csv("urban heat . csv")

print("Original Dataset:")
print(df.head(10))


# ================= 3. CHECK DATASET INFORMATION =================

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# ================= 4. CLEAN COLUMN NAMES =================

df.columns = df.columns.str.strip()


# ================= 5. REMOVE DUPLICATE ROWS =================

df = df.drop_duplicates()

print("\nDuplicate Rows Removed")


# ================= 6. CLEAN TEXT COLUMNS =================

text_columns = ["city", "country", "climate_zone"]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

df["climate_zone"] = df["climate_zone"].str.upper()


# ================= 7. CONVERT NUMERIC COLUMNS =================

numeric_columns = [
    "year",
    "lst_anomaly_c",
    "ndvi_mean",
    "impervious_pct",
    "tree_canopy_pct",
    "pop_density_km2",
    "heat_mortality_per_100k"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# ================= 8. HANDLE INVALID VALUES =================

# Percentage values must be between 0 and 100
for col in ["impervious_pct", "tree_canopy_pct"]:
    df.loc[~df[col].between(0, 100), col] = np.nan

# NDVI must be between -1 and 1
df.loc[~df["ndvi_mean"].between(-1, 1), "ndvi_mean"] = np.nan

# Population and mortality cannot be negative
df.loc[df["pop_density_km2"] < 0, "pop_density_km2"] = np.nan
df.loc[df["heat_mortality_per_100k"] < 0, "heat_mortality_per_100k"] = np.nan


# ================= 9. HANDLE MISSING VALUES =================

# Fill missing numerical values using median
for col in numeric_columns:
    median_value = df[col].median()
    df[col] = df[col].fillna(median_value)

# Fill missing text values using mode
for col in text_columns:
    mode_value = df[col].mode()
    if not mode_value.empty:
        df[col] = df[col].fillna(mode_value[0])
    else:
        df[col] = df[col].fillna("Unknown")


# ================= 10. CHECK CLEANED DATA =================

print("\nCleaned Dataset:")
print(df.head(10))

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nFinal Dataset Shape:")
print(df.shape)


# ================= 11. SAVE CLEANED CSV =================

df.to_csv("urban_heat_cleaned.csv", index=False)

print("\nData Cleaning Completed Successfully!")
print("Cleaned file saved as urban_heat_cleaned.csv")
    