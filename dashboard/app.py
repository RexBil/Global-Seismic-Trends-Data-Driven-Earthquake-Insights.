import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:Test%40123@localhost/seismic_db",
    pool_pre_ping=True
)

# -------------------------------------------------
# Function to load SQL queries
# -------------------------------------------------
def load_queries(path):
    queries = {}
    with open(path, "r") as file:
        sql = file.read()

    parts = sql.split("-- name:")
    for part in parts[1:]:
        name, query = part.split("\n", 1)
        queries[name.strip()] = query.strip()

    return queries

queries = load_queries("sql/analysis_queries.sql")

@st.cache_data
def run_query(query, _engine):
    with _engine.connect() as conn:
        return pd.read_sql(query, conn)


st.title("🌍 Global Seismic Trends Dashboard")

df = run_query("SELECT * FROM earthquakes", engine)

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

# -------------------------------------------------
# Run SQL Analysis Queries
# -------------------------------------------------

st.title("Magnitude & Depth")

# 1
st.subheader("Top 10 Strongest Earthquakes")
top10 = run_query(queries["top_10_strongest"], engine)
st.dataframe(top10)

# 2
st.subheader("Top 10 Deepest Earthquakes")
top10 = run_query(queries["top_10_depth_earthquakes"], engine)
st.dataframe(top10)

# 3
st.subheader("Shallow Strong Earthquakes")
shallow = run_query(queries["shallow_strong_earthquakes"], engine)
st.dataframe(shallow)

# 4
st.subheader("Average depth per continent")
avg_depth = run_query(queries["avg_depth_country"], engine)
st.dataframe(avg_depth)

# 5
st.subheader("Average Magnitude Per Country")
country = run_query(queries["avg_mag_country"], engine)
st.dataframe(country)


st.title("Time Analysis")

# 6
st.subheader("Year with Most Earthquakes")
year_most = run_query(queries["year_with_most_earthquakes"], engine)
st.dataframe(year_most)

# 7 
st.subheader("Month with highest number of earthquakes")
month = run_query(queries["month_highest_earthquakes"], engine)
st.dataframe(month)

# 8 
st.subheader("Day of week with most earthquakes")
day_week = run_query(queries["day_of_week_most_earthquakes"], engine)
st.dataframe(day_week)

# 9 
st.subheader("Count of earthquakes per hour of day")
count_earthquakes_hours = run_query(queries["count_earthquakes_per_hours_day"], engine)
st.dataframe(count_earthquakes_hours)

# 10 
st.subheader("Most active reporting network")
most_active_net = run_query(queries["most_active_net_work"], engine)
st.dataframe(most_active_net)


st.title("Casualties & Economic Loss")

# 11 
st.subheader("Top 5 places with highest casualtie")
top5 = run_query(queries["top_five_place"], engine)
st.dataframe(top5)

# 12 
st.subheader("Total estimated economic loss per continent")
total_est_eco = run_query(queries["total_estimated"], engine)
st.dataframe(total_est_eco)

# 13 
st.subheader("Average economic loss by alert level")
avg_eco = run_query(queries["avg_eco_loss"], engine)
st.dataframe(avg_eco)

st.title("Event Type & Quality Metrics")

# 14 
st.subheader("Count of reviewed vs automatic earthquakes")
count_review = run_query(queries["count_review_earthquakes"], engine)
st.dataframe(count_review)

# 15 
st.subheader("Count by earthquake type")
count_type = run_query(queries["count_earthquakes_type"], engine)
st.dataframe(count_type)

# 16 
st.subheader(" Number of earthquakes by data type")
number_earthquakas = run_query(queries["number_earthquakes"], engine)
st.dataframe(number_earthquakas)

# 17 
st.subheader("Average RMS and gap per continent")
avg_RMS_GAP = run_query(queries["avg_RMS_GAP"], engine)
st.dataframe(avg_RMS_GAP)

# 18 
st.subheader("Events with high station coverage")
event_high_station = run_query(queries["high_station_coverage"], engine)
st.dataframe(event_high_station)

st.title("Tsunamis & Alerts")
# 19
st.subheader("Number of tsunamis triggered per year")
tsunamis = run_query(queries["tsunami_count_per_year"], engine)
st.dataframe(tsunamis)

# 20 
st.subheader("Count earthquakes by alert levels")
alert_level = run_query(queries["alert_level"], engine)
st.dataframe(alert_level)

st.title("Seismic Pattern & Trends Analysis")
# 21 
st.subheader("Find the top 5 countries with the highest average magnitude of earthquakes in the past 10 years")
top5_highest_past_10_years = run_query(queries["highest_average_magnitude_10_years"], engine)
st.dataframe(top5_highest_past_10_years)

# 22 
st.subheader("Find countries that have experienced both shallow and deep earthquakes within the same month")
shallow_deep = run_query(queries["shallow_and_deep"], engine)
st.dataframe(shallow_deep)

# 23 
st.subheader("Compute the year-over-year growth rate in the total number of earthquakes globally")
year_over_year_growth_rate = run_query(queries["year_over_year_growth_rate"], engine)
st.dataframe(year_over_year_growth_rate)

# 24 
st.subheader("List the 3 most seismically active regions by combining both frequency and average magnitude")
most_3_seismically_active_regions = run_query(queries["most_3_seismically_active_regions"], engine)
st.dataframe(most_3_seismically_active_regions)

st.title("Depth, Location & Distance-Based  Analysis")
# 25 
st.subheader("For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator")
each_country = run_query(queries["avg_depth"], engine)
st.dataframe(each_country)

# 26 
st.subheader("Identify countries having the highest ratio of shallow to deep earthquakes")
highest_ratio = run_query(queries["highest_ratio"], engine)
st.dataframe(highest_ratio)

# 27 
st.subheader("Find the average magnitude difference between earthquakes with tsunami alerts and those without")
average_magnitude = run_query(queries["average_magnitude"], engine)
st.dataframe(average_magnitude)

# 28 
st.subheader("Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)")
lowest_data_reliability = run_query(queries["lowest_data_reliability"], engine)
st.dataframe(lowest_data_reliability)

# 29 
st.subheader("Find pairs of consecutive earthquakes (by time) that occurred within 50 km of each other and within 1 hour")
one_hours_within_50km = run_query(queries["one_hours_within_50km"], engine)
st.dataframe(one_hours_within_50km)

# 30
st.subheader("Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)")
determine_regions_with_the_highest_frequency = run_query(queries["determine_regions_with_the_highest_frequency"], engine)
st.dataframe(determine_regions_with_the_highest_frequency)



