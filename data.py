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
#client = storage.Client.from_service_account_json(key_path)
client = bigquery.Client(project="caabikeproject")

q = f"""
INSERT INTO `caabikeproject.BikeProject.geo-data`
(latitude, longitude)
VALUES('2025-03-12', '16:02:23')
"""
query_job = client.query(q)

q = """
SELECT * FROM `caabikeproject.BikeProject.geo-data`
LIMIT 10
"""

query_job = client.query(q)

df = query_job.to_dataframe()
print(df)