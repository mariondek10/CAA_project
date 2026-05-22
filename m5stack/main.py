import struct
from tomlkit import datetime
import ubinascii
import time
import sensor
import ui_interface
from machine import UART
import network
import urequests
import ujson
import time
from gps import GPS  # ton module GPS existant


# # Configuration
# lora = UART(1, baudrate=115200, rx=13, tx=14)

# def send_lora(lat, lon, speed, session): 
#     try:
#         # 1. Préparation du payload (10 octets au total)
#         # Lat (4) + Lon (4) + Speed (1) + Session (1) = 10 octets
#         payload_bytes = struct.pack('<iiBB', int(lat * 100000), int(lon * 100000), int(speed), session)
#         hex_payload = ubinascii.hexlify(payload_bytes).decode('utf-8').upper()
        
#         # 2. Construction de la commande AT+DTRX
#         payload_len = len(payload_bytes)
#         cmd_str = 'AT+DTRX=1,0,{},{}'.format(payload_len, hex_payload)
        
#         print("[LoRa] Envoi :", cmd_str)
#         lora.write((cmd_str + '\r\n').encode())
        
#         time.sleep(3) 
#         if lora.any():
#             resp = lora.read().decode('utf-8', 'ignore')
#             print("[LoRa] Réponse :", resp.strip())
#             return "SEND" in resp 
#         return False
#     except Exception as e:
#         print("[LoRa] Erreur d'envoi:", e)
#         return False
FLASK_URL = "http://<IP_DE_TON_PC>:8080/send-to-bigquery"
PASSWORD  = "M&M's"
SESSION_ID = 1  # incrémente à chaque sortie

'''def get_timestamp():
    t = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4], t[5]
    )'''

def send_data(lat, lon, speed, session_id):
    payload = {
        "passwd": PASSWORD,
        "values": {
            "latitude":   lat,
            "longitude":  lon,
            "timestamp": datetime.utcnow().isoformat(),
            "speed":      speed,
            "session_id": session_id
        }
    }
    try:
        r = urequests.post(
            FLASK_URL,
            data=ujson.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print("Réponse:", r.text)
        r.close()
    except Exception as e:
        print("Erreur envoi:", e)

# # --- DÉMARRAGE ---
ui_interface.init_screen()
print("Démarrage du système...")

# Boucle principale
while True:
    fix = sensor.read_gps(timeout_ms=500)
    if fix:
        lat, lon, spd = fix
        if spd < 5.0: spd = 0.0
        lat, lon, speed = gps.get_data()  # ta fonction existante
        if lat is not None:
            success = send_data(lat, lon, speed, SESSION_ID)
            ui_interface.update_display(speed, lat, lon, True, success)
    else:
        ui_interface.update_display(0.0, 0.0, 0.0, False, False)

    time.sleep(5)  # envoie toutes les 5 secondes

    
'''while True:
    fix = sensor.read_gps(timeout_ms=500)
    if fix:
        lat, lon, spd = fix
        if spd < 5.0: spd = 0.0
        
        # Envoi
        success = send_lora(lat, lon, spd, 1)
        ui_interface.update_display(spd, lat, lon, True, success)
    else:
        ui_interface.update_display(0.0, 0.0, 0.0, False, False)'''
    
#     # Pause de 60 secondes pour respecter la législation (Duty Cycle)
#     time.sleep(60)

# Lié à Flask 

# ---- Config ----






# ---- Boucle principale ----
