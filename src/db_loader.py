import pandas as pd
from db_config import get_engine

def load_to_mysql():
    engine = get_engine()
    df = pd.read_csv("data/processed/earthquakes_final.csv")

    df.to_sql("earthquakes", engine, if_exists="replace", index=False)
    print("✅ Data loaded into MySQL")

if __name__ == "__main__":
    load_to_mysql()
