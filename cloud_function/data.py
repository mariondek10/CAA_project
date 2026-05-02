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
VALUES(12.45, 18.45)
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
from machine import UART
import time

def get_gps_fix():
    gps = UART(2, baudrate=9600, rx=16, tx=17)
    start = time.ticks_ms()
    result = None
    while time.ticks_diff(time.ticks_ms(), start) < 2000:
        if gps.any():
            line = gps.readline()
            if line and b'$GPRMC' in line:
                result = line
                break
    gps.deinit()
    return result

def send_lora(payload):
    lora = UART(2, baudrate=115200, rx=16, tx=17)
    time.sleep_ms(100)  # let module wake up
    lora.write(f'AT+SEND={payload}\r\n'.encode())
    time.sleep_ms(500)
    response = lora.read() if lora.any() else None
    lora.deinit()
    return response

while True:
    # 1. Get GPS position
    fix = get_gps_fix()
    print("GPS:", fix)

    # 2. Send it over LoRa
    if fix:
        send_lora(fix.decode('utf-8', 'ignore').strip())

    time.sleep(30)


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