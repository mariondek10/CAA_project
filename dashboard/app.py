import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import plotly.express as px
from datetime import datetime
import os
import hashlib
from google.cloud import bigquery
import db_dtypes
import json
from google.cloud import secretmanager
from google.oauth2 import service_account

# # Accesses for local testing
# if os.path.exists("../../caabikeproject-ee4a905a2516.json"):
#    key_path = "../../caabikeproject-ee4a905a2516.json"
# else:
#    key_path = r"C:\Users\marin\bike_project\caabikeproject-ee4a905a2516.json"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

## Credentials for Cloud Run (using Secret Manager)

def get_bigquery_client():
    sm = secretmanager.SecretManagerServiceClient()
    # Utilise ton vrai nom de secret et ton project number
    name = "projects/387007830650/secrets/key-bikeProject/versions/latest"
    response = sm.access_secret_version(request={"name": name})
    key_dict = json.loads(response.payload.data.decode("UTF-8"))
    
    credentials = service_account.Credentials.from_service_account_info(key_dict)
    return bigquery.Client(project="caabikeproject", credentials=credentials)

client = get_bigquery_client()

PROJECT_NAME = "caabikeproject"

TABLE = f"{PROJECT_NAME}.BikeProject.geo_data"

st.set_page_config(
    page_title="Speed Dashboard",
    page_icon="🚲",
    layout="wide",
)
 
# Custom CSS 

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');
 
  html, body, [class*="css"] { font-family: 'DM Mono', monospace; }
  h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
 
  .metric-card {
    background: #414770;
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
  }
  .metric-label {
    font-size: 0.72rem;
    color: #6b7280;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .metric-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    color: #f0f4ff;
  }
  .metric-unit {
    font-size: 0.85rem;
    color: #9ca3af;
    margin-left: 0.25rem;
  }
  .highlight { color: #60a5fa; }
  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    color: #6b7280;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 1.5rem 0 0.5rem;
    border-bottom: 1px solid #2a2d3a;
    padding-bottom: 0.4rem;
  }
</style>
""", unsafe_allow_html=True)
 
 
@st.cache_resource
def get_client():
    return bigquery.Client(project=PROJECT_NAME)
 
## Data access functions 
def run_query(sql: str) -> pd.DataFrame:
    return get_client().query(sql).to_dataframe()
 

## Cached queries for session list and session data 
@st.cache_data(ttl=300)
def get_sessions() -> list[int]:
    df = run_query(f"SELECT DISTINCT session_id FROM `{TABLE}` ORDER BY session_id DESC")
    return df["session_id"].tolist()
 

## Cache session data for 5 minutes to speed up UI interactions when re-selecting sessions 
@st.cache_data(ttl=300)
def get_session_data(session_id: int) -> pd.DataFrame:
    return run_query(f"""
        SELECT latitude, longitude, timestamp, speed
        FROM `{TABLE}`
        WHERE session_id = {session_id}
        ORDER BY timestamp ASC
    """)
 

## Data processing functions (speed zones, distance calculation, duration formatting) 
def haversine_series(df: pd.DataFrame) -> float:
    """Total distance in km using the Haversine formula."""
    R = 6371
    lat = np.radians(df["latitude"].values)
    lon = np.radians(df["longitude"].values)
    dlat = np.diff(lat)
    dlon = np.diff(lon)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat[:-1]) * np.cos(lat[1:]) * np.sin(dlon / 2) ** 2
    return float(np.sum(2 * R * np.arcsin(np.sqrt(a))))
 

## Format duration as "Xm Ys" or "Xh Ym" 
def duration_str(df: pd.DataFrame) -> str:
    ts = pd.to_datetime(df["timestamp"])
    delta = ts.max() - ts.min()
    total_s = int(delta.total_seconds())
    h, rem = divmod(total_s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"
 

## Classify speed samples into zones (km/h) with the same emojis as the m5stack display for fun :) 
def speed_zone_distribution(df: pd.DataFrame) -> dict:
    """Classify speed samples into zones (km/h)."""
    spd = df["speed"].dropna()
    zones = {
        "🐢 Easy  (<15)": (spd < 15).sum(),
        "🐰 Moderate (15–25)": ((spd >= 15) & (spd < 25)).sum(),
        "🦁 Hard  (>25)": ((spd >= 25).sum())
    }
    return zones
 
 
# App layout
st.title("🚲 Speed tracker Dashboard")
st.caption("Your personal cycling analytics hub")
 
# Sidebar – session selector
with st.sidebar:
    st.header("Session")
    sessions = get_sessions()
    if not sessions:
        st.error("No sessions found in BigQuery. You need to record some rides first! 🚴‍♂️")
        st.stop()
 
    selected = st.selectbox(
        "Choose a session",
        sessions,
        format_func=lambda x: f"Session #{x}",
    )
    st.divider()
    st.caption(f"{len(sessions)} sessions recorded")

    # Session suppression button
    st.divider()
    if st.button("🗑️ Delete this session", use_container_width=True):
        # BigQuery DELETE query to remove all data points of the selected session
        delete_query = f"DELETE FROM `{TABLE}` WHERE session_id = {selected}"
        client.query(delete_query).result() # Le .result() attend que l'action soit finie
        
        st.cache_data.clear()
        st.success(f"Session #{selected} deleted successfully!")
        time.sleep(1.5)
        st.rerun()
 
# Load data
df = get_session_data(selected)
 
if df.empty:
    st.warning("No data for this session.")
    st.stop()
 
# KPI row 
st.markdown(f"### Session **#{selected}**")
 
distance_km = haversine_series(df)
avg_speed   = df["speed"].mean()
max_speed   = df["speed"].max()
duration    = duration_str(df)
data_points = len(df)
 
cols = st.columns(5)
metrics = [
    ("Distance",      f"{distance_km:.2f}", "km"),
    ("Duration",      duration,             ""),
    ("Avg speed",     f"{avg_speed:.1f}",   "km/h"),
    ("Max speed",     f"{max_speed:.1f}",   "km/h"),
    ("GPS points",    f"{data_points:,}",   "pts"),
]
for col, (label, value, unit) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value highlight">{value}<span class="metric-unit">{unit}</span></div>
        </div>
        """, unsafe_allow_html=True)
 
# Map trace 
# st.markdown('<div class="section-title">🗺 Route trace</div>', unsafe_allow_html=True)
# map_df = df[["latitude", "longitude"]].dropna().rename(
#     columns={"latitude": "lat", "longitude": "lon"}
# )
# st.map(map_df, size=4, color="#60a5fa")
 

# Map trace 
st.markdown('<div class="section-title">🗺 Route trace</div>', unsafe_allow_html=True)

# On filtre les éventuelles coordonnées nulles qui fausseraient la carte
map_df = df[(df["latitude"] != 0.0) & (df["longitude"] != 0.0)]

if not map_df.empty:
    # Création d'une ligne sur une carte au style sombre
    fig = px.line_mapbox(
        map_df, 
        lat="latitude", 
        lon="longitude", 
        color_discrete_sequence=["#60a5fa"], 
        zoom=13
    )
    
    # Configuration du fond de carte
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Waiting for valid GPS coordinates to draw the map...")

# Speed chart 
st.markdown('<div class="section-title">⚡ Speed over time</div>', unsafe_allow_html=True)
speed_df = df[["timestamp", "speed"]].dropna().set_index("timestamp")
st.line_chart(speed_df, color="#60a5fa")
 
# Speed zone distribution 
st.markdown('<div class="section-title">🏷 Speed zone distribution</div>', unsafe_allow_html=True)
zones = speed_zone_distribution(df)
zone_df = pd.DataFrame.from_dict(
    zones, orient="index", columns=["samples"]
).reset_index().rename(columns={"index": "zone"})
zone_df["pct"] = (zone_df["samples"] / zone_df["samples"].sum() * 100).round(1)
st.dataframe(
    zone_df,
    hide_index=True,
    column_config={
        "zone":    st.column_config.TextColumn("Zone"),
        "samples": st.column_config.NumberColumn("Samples", format="%d"),
        "pct":     st.column_config.ProgressColumn("Share (%)", min_value=0, max_value=100),
    },
    use_container_width=True,
)

# Pace analysis with speed zones and distance by zone thanks to SQL query
st.markdown('<div class="section-title">📊 All-session overview</div>', unsafe_allow_html=True)
 
@st.cache_data(ttl=300)
def get_all_sessions_summary() -> pd.DataFrame:
    return run_query(f"""
        SELECT
          session_id,
          COUNT(*)                                    AS gps_points,
          ROUND(AVG(speed), 2)                        AS avg_speed_kmh,
          ROUND(MAX(speed), 2)                        AS max_speed_kmh,
          TIMESTAMP_DIFF(MAX(timestamp), MIN(timestamp), SECOND) AS duration_sec
        FROM `{TABLE}`
        GROUP BY session_id
        ORDER BY session_id DESC
    """)
 
summary = get_all_sessions_summary()
summary["duration_min"] = (summary["duration_sec"] / 60).round(1)
st.dataframe(
    summary.drop(columns=["duration_sec"]),
    hide_index=True,
    column_config={
        "session_id":    st.column_config.NumberColumn("Session"),
        "gps_points":    st.column_config.NumberColumn("GPS pts"),
        "avg_speed_kmh": st.column_config.NumberColumn("Avg speed (km/h)"),
        "max_speed_kmh": st.column_config.NumberColumn("Max speed (km/h)"),
        "duration_min":  st.column_config.NumberColumn("Duration (min)"),
    },
    use_container_width=True,
)
 
# Raw data expander to have the replication of the BigQuery table view for each session
with st.expander("🔍 Raw session data"):
    st.dataframe(df, use_container_width=True)
 
    