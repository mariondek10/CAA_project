import sensor
import ui_interface
import bq_client
import math
import time

ui_interface.show_boot_screen()
time.sleep(2)
ui_interface.init_screen()

prev_lat, prev_lon, prev_time = None, None, None
last_send = time.ticks_ms()
SEND_INTERVAL = 10000  # envoie toutes les 10 secondes

def haversine(lat1, lon1, lat2, lon2):
    import math
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

print("Tracker started")
while True:
    fix = sensor.read_gps(timeout_ms=1000)
    if fix:
        lat, lon = fix
        now = time.ticks_ms()
        if prev_lat is not None:
            dt = time.ticks_diff(now, prev_time)
            dist = haversine(prev_lat, prev_lon, lat, lon)
            speed = (dist / (dt / 1000)) * 3.6
        else:
            speed = 0.0
        prev_lat, prev_lon, prev_time = lat, lon, now

        # Envoi BigQuery toutes les 10s
        if time.ticks_diff(now, last_send) >= SEND_INTERVAL:
            lora_ok = bq_client.send_to_bigquery(lat, lon, speed)
            last_send = now
            ui_interface.update_display(speed, lat, lon, True, lora_ok)
        else:
            ui_interface.update_display(speed, lat, lon, True, False)

        print("GPS: {:.6f},{:.6f} | {:.1f} km/h".format(lat, lon, speed))
    else:
        ui_interface.update_display(0.0, 0.0, 0.0, False, False)
        print("No fix")
    time.sleep_ms(200)