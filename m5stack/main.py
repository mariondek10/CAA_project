# import struct
# from tomlkit import datetime
# import ubinascii
# import time
# import sensor
# import ui_interface
# from machine import UART
# import network
# import urequests
# import ujson
# import time
# from gps import GPS  # ton module GPS existant


# # # Configuration
# # lora = UART(1, baudrate=115200, rx=13, tx=14)

# # def send_lora(lat, lon, speed, session): 
# #     try:
# #         # 1. Préparation du payload (10 octets au total)
# #         # Lat (4) + Lon (4) + Speed (1) + Session (1) = 10 octets
# #         payload_bytes = struct.pack('<iiBB', int(lat * 100000), int(lon * 100000), int(speed), session)
# #         hex_payload = ubinascii.hexlify(payload_bytes).decode('utf-8').upper()
        
# #         # 2. Construction de la commande AT+DTRX
# #         payload_len = len(payload_bytes)
# #         cmd_str = 'AT+DTRX=1,0,{},{}'.format(payload_len, hex_payload)
        
# #         print("[LoRa] Envoi :", cmd_str)
# #         lora.write((cmd_str + '\r\n').encode())
        
# #         time.sleep(3) 
# #         if lora.any():
# #             resp = lora.read().decode('utf-8', 'ignore')
# #             print("[LoRa] Réponse :", resp.strip())
# #             return "SEND" in resp 
# #         return False
# #     except Exception as e:
# #         print("[LoRa] Erreur d'envoi:", e)
# #         return False
# FLASK_URL = "http://192.168.1.176:8080/send-to-bigquery"
# PASSWORD  = "M&M's"
# SESSION_ID = 1  # incrémente à chaque sortie

# '''def get_timestamp():
#     t = time.localtime()
#     return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
#         t[0], t[1], t[2], t[3], t[4], t[5]
#     )'''

# def send_data(lat, lon, speed, session_id):
#     payload = {
#         "passwd": PASSWORD,
#         "values": {
#             "latitude":   lat,
#             "longitude":  lon,
#             "timestamp": datetime.utcnow().isoformat(),
#             "speed":      speed,
#             "session_id": session_id
#         }
#     }
#     try:
#         r = urequests.post(
#             FLASK_URL,
#             data=ujson.dumps(payload),
#             headers={"Content-Type": "application/json"},
#             timeout=5
#         )
#         print("Réponse:", r.text)
#         r.close()
#     except Exception as e:
#         print("Erreur envoi:", e)

# # # --- DÉMARRAGE ---
# ui_interface.init_screen()
# print("Démarrage du système...")

# # Boucle principale
# while True:
#     fix = sensor.read_gps(timeout_ms=500)
#     if fix:
#         lat, lon, spd = fix
#         if spd < 5.0: spd = 0.0
#         lat, lon, speed = sensor.read_gps()  
#         if lat is not None:
#             success = send_data(lat, lon, speed, SESSION_ID)
#             ui_interface.update_display(speed, lat, lon, True, success)
#     else:
#         ui_interface.update_display(0.0, 0.0, 0.0, False, False)

#     time.sleep(5)  # envoie toutes les 5 secondes

    
# '''while True:
#     fix = sensor.read_gps(timeout_ms=500)
#     if fix:
#         lat, lon, spd = fix
#         if spd < 5.0: spd = 0.0
        
#         # Envoi
#         success = send_lora(lat, lon, spd, 1)
#         ui_interface.update_display(spd, lat, lon, True, success)
#     else:
#         ui_interface.update_display(0.0, 0.0, 0.0, False, False)'''
    
# #     # Pause de 60 secondes pour respecter la législation (Duty Cycle)
# #     time.sleep(60)

# # Lié à Flask 

# # ---- Config ----






# # ---- Boucle principale ----

import struct
import ubinascii
import time
import sensor
import ui_interface
from machine import UART
import network
import urequests
import ujson

# # --- DÉMARRAGE DE L'ÉCRAN ---
ui_interface.init_screen()
print("Démarrage du système...")

# ---- CONFIGURATION ----
FLASK_URL = "https://bike-backend-387007830650.europe-west6.run.app"
PASSWORD  = "M&M's"

# ---- GESTION AUTOMATIQUE DE LA SESSION (Fichier local) ----
SESSION_FILE = "session.txt"

def get_and_increment_session():
    try:
        # 1. Essayer de lire la dernière session
        with open(SESSION_FILE, "r") as f:
            current_session = int(f.read().strip())
    except Exception:
        # Si le fichier n'existe pas encore, on commence à 0
        current_session = 0
    
    # 2. Incrémenter pour la sortie actuelle
    new_session = current_session + 1
    
    # 3. Sauvegarder le nouveau numéro dans la mémoire de la carte
    try:
        with open(SESSION_FILE, "w") as f:
            f.write(str(new_session))
    except Exception as e:
        print("Erreur écriture session.txt:", e)
        
    return new_session

# Récupération de l'ID unique de cette sortie
SESSION_ID = get_and_increment_session()
print("=== SESSION EN COURS : #{} ===".format(SESSION_ID))

buffer = []

def is_connected():
    wlan = network.WLAN(network.STA_IF)
    return wlan.isconnected()

def send_data(lat, lon, speed, session_id):
    payload = {
        "passwd": PASSWORD,
        "values": {
            "latitude":   lat,
            "longitude":  lon,
            "speed":      speed,
            "session_id": session_id
        }
    }
    try:
        r = urequests.post(
            FLASK_URL,
            data=ujson.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        print("Réponse Flask:", r.text)
        r.close()
        return True
    except Exception as e:
        print("Erreur envoi Flask:", e)
        return False

if not is_connected():
    print("Pas de Wi-Fi, stockage en mémoire tampon activé.")

# ---- BOUCLE PRINCIPALE ----
while True:
    fix = sensor.read_gps()
    
    if fix is not None:
        lat, lon, speed = fix
        if speed < 5.0: 
            speed = 0.0
            
        print("GPS OK: {:.6f}, {:.6f} | Vitesse: {:.1f} km/h".format(lat, lon, speed))
        buffer.append((lat, lon, speed))
        gps_active = True
    else:
        print("En attente de signal GPS...")
        lat, lon, speed = 0.0, 0.0, 0.0
        gps_active = False

    success_envoi = False
    if is_connected() and buffer:
        print("[Wi-Fi] Envoi de {} points en mémoire...".format(len(buffer)))
        for point in buffer[:]:
            b_lat, b_lon, b_speed = point
            success_envoi = send_data(b_lat, b_lon, b_speed, SESSION_ID)
            if success_envoi:
                buffer.remove(point)
            time.sleep(0.2)

    ui_interface.update_display(speed, lat, lon, gps_active, success_envoi)
    time.sleep(5)