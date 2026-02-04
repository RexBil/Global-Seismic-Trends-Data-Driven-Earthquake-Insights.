import os
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

def fetch_earthquake_data(start_date, end_date, min_magnitude=4.5):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    all_records = []

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while start < end:
        next_month = start + timedelta(days=30)

        params = {
            "format": "geojson",
            "starttime": start.strftime("%Y-%m-%d"),
            "endtime": next_month.strftime("%Y-%m-%d"),
            "minmagnitude": min_magnitude,
            "limit": 20000
        }

        print(f"Fetching: {params['starttime']} → {params['endtime']}")

        response = requests.get(url, params=params, timeout=30)

        if response.status_code != 200:
            print("⚠️ Bad response:", response.status_code)
            start = next_month
            continue

        try:
            data = response.json()
        except ValueError:
            print("⚠️ Invalid JSON, skipping")
            start = next_month
            continue

        for feature in data.get("features", []):
            prop = feature.get("properties", {})
            geo = feature.get("geometry", {})
            coords = geo.get("coordinates", [None, None, None])

            all_records.append({
                "id": feature.get("id"),

                # ✅ timezone-aware datetime
                "time": datetime.fromtimestamp(prop.get("time", 0) / 1000, timezone.utc),
                "updated": datetime.fromtimestamp(prop.get("updated", 0) / 1000, timezone.utc),

                "latitude": coords[1],
                "longitude": coords[0],
                "depth_km": coords[2],

                "mag": prop.get("mag"),
                "magType": prop.get("magType"),
                "place": prop.get("place"),
                "status": prop.get("status"),
                "tsunami": prop.get("tsunami"),
                "sig": prop.get("sig"),
                "net": prop.get("net"),

                # ✅ SAFE optional fields
                "nst": prop.get("nst"),
                "dmin": prop.get("dmin"),
                "rms": prop.get("rms"),
                "gap": prop.get("gap"),
                "magError": prop.get("magError"),
                "depthError": prop.get("depthError"),
                "magNst": prop.get("magNst"),

                "locationSource": prop.get("locationSource"),
                "magSource": prop.get("magSource"),
                "types": prop.get("types"),
                "ids": prop.get("ids"),
                "sources": prop.get("sources"),
                "type": prop.get("type")
            })

        start = next_month

    df = pd.DataFrame(all_records)
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/earthquakes_raw.csv", index=False)

    print(f"✅ Total records fetched: {len(df)}")
    return df


if __name__ == "__main__":
    fetch_earthquake_data("2020-01-01", "2025-01-01")
