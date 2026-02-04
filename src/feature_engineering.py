import pandas as pd
import os

def engineer_features():
    df = pd.read_csv("data/processed/earthquakes_cleaned.csv")

    # ✅ SAFE datetime parsing (timezone-aware)
    df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")

    # Drop rows where time could not be parsed (very few)
    df = df.dropna(subset=["time"])

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["day_of_week"] = df["time"].dt.day_name()

    df["depth_category"] = df["depth_km"].apply(
        lambda x: "Shallow" if x < 70 else "Intermediate" if x < 300 else "Deep"
    )

    df["strong_eq"] = df["mag"].apply(lambda x: 1 if x >= 7.0 else 0)

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/earthquakes_final.csv", index=False)

    print("✅ Feature engineering completed successfully")
    return df


if __name__ == "__main__":
    engineer_features()
