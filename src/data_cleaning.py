import os
import pandas as pd
import re

def extract_country(place):
    if pd.isna(place):
        return "Unknown"
    match = re.search(r",\s*(.*)", place)
    return match.group(1) if match else "Unknown"

def clean_data():
    df = pd.read_csv("data/raw/earthquakes_raw.csv")

    df["country"] = df["place"].apply(extract_country)

    numeric_cols = [
        "mag", "depth_km", "nst", "dmin", "rms",
        "gap", "magError", "depthError", "magNst", "sig"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/earthquakes_cleaned.csv", index=False)
    return df

if __name__ == "__main__":
    clean_data()
