import time
import sensor
import ui_interface
import network
import urequests
import ujson
from m5stack import touch, btnA, btnC

# --- Config ---
WIFI_SSID = "iPhone (48)"  
WIFI_PASS = "09651234"          
FLASK_URL = "https://bike-backend-387007830650.europe-west6.run.app/send-to-bigquery"
PASSWORD  = "M&M's"
SESSION_FILE = "session.txt"

# --- Wi-Fi Setup ---
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to {}...".format(ssid))
        wlan.connect(ssid, password)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    return wlan.isconnected()

def run_wifi_interactive_config():
    """ Handles interactive Wi-Fi config on startup if screen is touched """
    ui_interface.show_config_prompt()
    start_time = time.time()
    touch_detected = False
    
    # Wait 5s for user touch
    while time.time() - start_time < 5:
        if touch.status(): 
            touch_detected = True
            break
        time.sleep(0.1)
        
    if touch_detected:
        print("Scan mode activated!")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        try:
            scan_results = wlan.scan()
            networks_found = [res[0].decode('utf-8') for res in scan_results if res[0]]
        except Exception:
            networks_found = ["iPhone (48)", "UNIL-Campus", "EPFL-Guest"]
            
        ui_interface.show_wifi_menu(networks_found)
        time.sleep(4) 
        
    ui_interface.show_connecting_screen(WIFI_SSID)
    connect_wifi(WIFI_SSID, WIFI_PASS)

# --- Session Management ---
def get_and_increment_session():
    """ Reads last session ID from file and increments it """
    try:
        with open(SESSION_FILE, "r") as f:
            current = int(f.read().strip())
    except Exception:
        current = 0
    new_session = current + 1
    try:
        with open(SESSION_FILE, "w") as f:
            f.write(str(new_session))
    except Exception:
        pass
    return new_session

def send_data(lat, lon, speed, session_id):
    """ Sends payload to Flask backend """
    payload = {
        "passwd": PASSWORD,
        "values": {
            "latitude": lat, "longitude": lon, 
            "speed": speed, "session_id": session_id
        }
    }
    try:
        r = urequests.post(FLASK_URL, data=ujson.dumps(payload), headers={"Content-Type": "application/json"})
        r.close()
        return True
    except Exception:
        return False

def is_connected():
    return network.WLAN(network.STA_IF).isconnected()

# --- Boot Sequence ---
ui_interface.show_boot_screen()
time.sleep(1.5)
run_wifi_interactive_config()
ui_interface.init_screen()

# --- State Variables ---
session_state = "STOPPED" # States: STOPPED, RUNNING, PAUSED
speed_history = []
buffer = []
SESSION_ID = 0

# --- Main Loop ---
while True:
    # 1. Controls (A = Start/Pause/Resume, C = Stop)
    if btnA.wasPressed():
        if session_state == "STOPPED":
            SESSION_ID = get_and_increment_session()
            session_state = "RUNNING"
            buffer.clear()
            speed_history.clear()
            print("▶️ START SESSION: #{}".format(SESSION_ID))            
        elif session_state == "RUNNING":
            session_state = "PAUSED"
            print("⏸️ PAUSED")
            
        elif session_state == "PAUSED":
            session_state = "RUNNING"
            print("▶️ RESUMED")

    if btnC.wasPressed():
        if session_state != "STOPPED":
            print("⏹️ STOPPED")
            session_state = "STOPPED"
            # Flush remaining buffer before stopping
            if is_connected() and buffer:
                for p in buffer[:]:
                    send_data(p[0], p[1], p[2], SESSION_ID)
            buffer.clear()

    # 2. GPS 
    fix = sensor.read_gps()
    wifi_status = is_connected()
    
    if fix is not None:
        lat, lon, raw_speed = fix
        
        if raw_speed < 1.0: 
            raw_speed = 0.0
            
        # Moving average (last 2 values) for stable speed display
        speed_history.append(raw_speed)
        if len(speed_history) > 2:
            speed_history.pop(0)
        speed = sum(speed_history) / len(speed_history)
        
        gps_active = True
        
        # Only record data if session is active
        if session_state == "RUNNING":
            buffer.append((lat, lon, speed))
    else:
        lat, lon, speed = 0.0, 0.0, 0.0
        gps_active = False

    # 3. Background Data Transmission
    success_envoi = False
    if wifi_status and buffer:
        for point in buffer[:]:
            b_lat, b_lon, b_speed = point
            success_envoi = send_data(b_lat, b_lon, b_speed, SESSION_ID)
            if success_envoi:
                buffer.remove(point)
            time.sleep(0.2)

    ui_interface.update_display(speed, lat, lon, gps_active, wifi_status, session_state)
    for _ in range(50):
        time.sleep(0.1)
        if btnA.wasPressed() or btnC.wasPressed():
            break 
# --------------------------------------------------------------------------------
# LoRa test implementation
# --------------------------------------------------------------------------------
# import struct
# import ubinascii
# from machine import UART
# lora = UART(1, baudrate=115200, rx=13, tx=14)
#
# def send_lora(lat, lon, speed, session): 
#     try:
#         payload_bytes = struct.pack('<iiBB', int(lat * 100000), int(lon * 100000), int(speed), session)
#         hex_payload = ubinascii.hexlify(payload_bytes).decode('utf-8').upper()
#         cmd_str = 'AT+DTRX=1,0,{},{}'.format(len(payload_bytes), hex_payload)
#         lora.write((cmd_str + '\r\n').encode())
#         time.sleep(3) 
#         if lora.any():
#             resp = lora.read().decode('utf-8', 'ignore')
#             return "SEND" in resp 
#         return False
#     except Exception as e:
#         return False
# 
# # Inside loop:
# # success = send_lora(lat, lon, spd, 1)
# # ui_interface.update_display(spd, lat, lon, True, success)
