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



#M5 flow python code
'''
setScreenColor(0x29aa54)
gps_0 = unit.get(unit.GPS, unit.PORTC)

gps_long = M5TextBox(179, 85, "label0", lcd.FONT_Default, 0xFFFFFF, rotate=0)
longText = M5TextBox(88, 85, "Longitude :", lcd.FONT_Default, 0xFFFFFF, rotate=0)
lat_text = M5TextBox(88, 119, "Latitude :", lcd.FONT_Default, 0xFFFFFF, rotate=0)
gps_lat = M5TextBox(179, 119, "label2", lcd.FONT_Default, 0xFFFFFF, rotate=0)

date = M5TextBox(88, 150, "Date", lcd.FONT_Default, 0xFFFFFF, rotate=0)


gps_0.uart_port_id(1)
gps_long.setText(str(gps_0.longitude))
gps_lat.setText(str(gps_0.latitude))
date.setText(str(gps_0.gps_date))

print(gps_0.latitude)
'''