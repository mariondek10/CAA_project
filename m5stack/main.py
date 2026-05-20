import struct
import ubinascii
import time
import sensor
import ui_interface
from machine import UART

# Configuration
lora = UART(1, baudrate=115200, rx=33, tx=32)

def send_lora(lat, lon, speed, session): 
    try:
        # 1. Préparation du payload (10 octets au total)
        # Lat (4) + Lon (4) + Speed (1) + Session (1) = 10 octets
        payload_bytes = struct.pack('<iiBB', int(lat * 100000), int(lon * 100000), int(speed), session)
        hex_payload = ubinascii.hexlify(payload_bytes).decode('utf-8').upper()
        
        # 2. Construction de la commande AT+DTRX
        # Syntaxe: AT+DTRX=Port,Confirmé(0),LongueurBytes,PayloadHex
        payload_len = len(payload_bytes)
        cmd_str = 'AT+DTRX=1,0,{},{}'.format(payload_len, hex_payload)
        
        print("[LoRa] Envoi :", cmd_str)
        lora.write((cmd_str + '\r\n').encode())
        
        # 3. Attente courte pour le résultat
        time.sleep(3) 
        if lora.any():
            resp = lora.read().decode('utf-8', 'ignore')
            print("[LoRa] Réponse :", resp.strip())
            return "SEND" in resp # Si on a reçu SEND:xx, c'est bon
        return False
    except Exception as e:
        print("[LoRa] Erreur d'envoi:", e)
        return False

# --- DÉMARRAGE ---
ui_interface.init_screen()
print("Démarrage du système...")

# Boucle principale
while True:
    fix = sensor.read_gps(timeout_ms=500)
    if fix:
        lat, lon, spd = fix
        if spd < 5.0: spd = 0.0
        
        # Envoi
        success = send_lora(lat, lon, spd, 1)
        ui_interface.update_display(spd, lat, lon, True, success)
    else:
        ui_interface.update_display(0.0, 0.0, 0.0, False, False)
    
    # Pause de 60 secondes pour respecter la législation (Duty Cycle)
    time.sleep(60)
