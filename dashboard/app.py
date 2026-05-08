import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import os
import hashlib
from google.cloud import bigquery
import db_dtypes
key_path = "../caabikeproject-ee4a905a2516.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
PROJECT_NAME = "caabikeproject"

#client = storage.Client.from_service_account_json(key_path)
client = bigquery.Client(project=PROJECT_NAME)

dataset_ref = client.dataset("BikeProject", project=PROJECT_NAME)

dataset = client.get_dataset(dataset_ref)
tables = list(client.list_tables(dataset))

table_ref = dataset_ref.table("movies")
movies_table = client.get_table(table_ref)



def run_query(sql: str) -> pd.DataFrame:

    # display the SQL in the terminal
    print("\n Executing SQL: ")
    print(sql)
    return client.query(sql).to_dataframe()


def get_bike_data()-> list[str]:
    df = run_query(
        "select * from {}.BikeProject.geo_data".format(PROJECT_NAME)
    )
    return [row.language for row in df.itertuples() if row.language] or []

    

def main():
    st.set_page_config(
    page_title="Bike Dashboard",
    page_icon="🚲",
)
    st.title("🚲 Welcome to your biking Dashboard!")
    st.write("Here is an overview of all your biking session:")
    st.map()
    st.subheader("Your Recent Biking Session:")
    # Display a selecter that allows the user to choose a time range for their biking sessions
    st.selectbox("Select a time range for your biking sessions:", options=["Last Week", "Last Month", "Last Year"])
    st.dataframe({
        "Distance q(km)": [15.2],
        "Duration (min)": [45],
        "Average Speed (km/h)": [20.3],
        "Calories Burned": [350]
    })

if __name__ == "__main__":
    main()

    