import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:Test%40123@localhost/seismic_db"
)

st.title("🌍 Global Seismic Trends Dashboard")

df = pd.read_sql("SELECT * FROM earthquakes", engine)

year = st.selectbox("Select Year", sorted(df["year"].unique()))
filtered = df[df["year"] == year]

fig = px.histogram(filtered, x="mag", nbins=20, title="Magnitude Distribution")
st.plotly_chart(fig)

fig2 = px.scatter(
    filtered,
    x="longitude",
    y="latitude",
    size="mag",
    color="depth_category",
    title="Earthquake Locations"
)
st.plotly_chart(fig2)
