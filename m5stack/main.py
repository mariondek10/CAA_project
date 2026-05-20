import sensor
import ui_interface
import time
import math  
from machine import UART

# --- 1. GESTION DE LA SESSION ---
FICHIER_SESSION = "last_session.txt"
def get_next_session_id():
    try:
        with open(FICHIER_SESSION, "r") as f: last_id = int(f.read())
    except:
        last_id = 0
    new_id = last_id + 1
    with open(FICHIER_SESSION, "w") as f: f.write(str(new_id))
    return new_id

SESSION_ID = get_next_session_id()

# --- 2. FONCTION DE CALCUL DE VITESSE (HAVERSINE) ---
def haversine(lat1, lon1, lat2, lon2, dt_ms):
    if dt_ms <= 0: return 0.0
    # Rayon de la Terre en km
    R = 6371.0
    phi1, phi2 = lat1 * math.pi / 180, lat2 * math.pi / 180
    dphi = (lat2 - lat1) * math.pi / 180
    dlambda = (lon2 - lon1) * math.pi / 180
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    dist = 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Vitesse en km/h
    return dist / (dt_ms / 3600000.0)

# --- 3. CONFIGURATION LORA (PORT ROUGE) ---
# On utilise UART 1, Pins 33(RX) et 32(TX)
lora = UART(1, baudrate=115200, rx=33, tx=32)

print("Lancement du JOIN LoRaWAN...")
lora.write('AT+CJOIN=1,0,10,8\r\n'.encode())
def send_lora(lat, lon, speed, session): 
    try:
        payload = "{:.4f},{:.4f},{:.1f},{}".format(lat, lon, speed, session)
        cmd = 'AT+CMSG="{}"\r\n'.format(payload)
        print("\n[LoRa] Envoi :", cmd.strip())
        lora.write(cmd.encode())
        
        time.sleep_ms(600) # On laisse un peu plus de temps pour la réponse
        
        if lora.any():
            resp = lora.read().decode('utf-8', 'ignore')
            print("[LoRa] Réponse :", resp.strip())
            # Si la réponse contient OK et PAS d'erreur, c'est gagné
            if "OK" in resp and "ERROR" not in resp:
                return True
        return False
    except:
        return False

# --- 4. INITIALISATION ---
ui_interface.init_screen()
prev_lat, prev_lon, prev_time = None, None, None
last_send = time.ticks_ms()
last_lora_status = False
gps_locked = False

# --- 5. BOUCLE PRINCIPALE ---
while True:
    now = time.ticks_ms()
    fix = sensor.read_gps(timeout_ms=500)
    
    if fix:
        lat, lon = fix
        gps_locked = True
        
        # Calcul de la vitesse réelle
        current_speed = 0.0
        if prev_lat is not None:
            dt = time.ticks_diff(now, prev_time)
            current_speed = haversine(prev_lat, prev_lon, lat, lon, dt)
            # Filtre : si la vitesse est aberrante ou trop faible, on met 0
            if current_speed < 1.5: current_speed = 0.0
            
        prev_lat, prev_lon, prev_time = lat, lon, now

        # Envoi LoRa toutes les 10 secondes
        if time.ticks_diff(now, last_send) >= 10000:
            last_lora_status = send_lora(lat, lon, current_speed, SESSION_ID)
            last_send = time.ticks_ms()
            
        ui_interface.update_display(current_speed, lat, lon, True, last_lora_status)
    else:
        # On garde le dernier statut LoRa même si le GPS cherche
        ui_interface.update_display(0.0, 0.0, 0.0, False, last_lora_status)
