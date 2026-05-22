import struct
import ubinascii
import time
import sensor
import ui_interface
from machine import UART

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

# # --- DÉMARRAGE ---
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
    
#     # Pause de 60 secondes pour respecter la législation (Duty Cycle)
#     time.sleep(60)

# import time
# import network
# import urequests  
# import sensor
# import ui_interface

# # --- 1. CONFIGURATION WI-FI & GOOGLE CLOUD ---
# SSID = "iPhone (48)"          # <--- Mets le nom de ton partage de co
# PASSWORD = "09651234"        # <--- Mets ton mot de passe
# URL_CLOUD = "https://function-retrieve-geo-data-387007830650.europe-west6.run.app" # <--- Colle ton URL Google Cloud ici

# # Initialisation de l'interface graphique
# ui_interface.init_screen()

# # Configuration du Wi-Fi
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)

# def gerer_connexion_wifi():
#     """Gère la connexion et renvoie l'état du Wi-Fi"""
#     if not wlan.isconnected():
#         wlan.connect(SSID, PASSWORD)
#         timeout = 5
#         while not wlan.isconnected() and timeout > 0:
#             time.sleep(1)
#             timeout -= 1
#     return wlan.isconnected()

# # --- 2. AFFICHAGE DU STATUT DE DÉMARRAGE ---
# print("Tentative de connexion Wi-Fi initiale...")
# if gerer_connexion_wifi():
#     # Si le Wi-Fi marche au démarrage, on peut l'écrire temporairement sur la console/écran
#     print("Wi-Fi OK au démarrage")
# else:
#     print("Wi-Fi NON TROUVÉ au démarrage")

# # --- 3. FONCTION D'ENVOI WI-FI (Simule le comportement du voyant) ---
# def send_via_wifi(lat, lon, spd, session):
#     if not wlan.isconnected():
#         return False
#     try:
#         payload_txt = "{:.4f},{:.4f},{:.1f},{}".format(lat, lon, spd, session)
#         headers = {'Content-Type': 'text/plain'}
        
#         response = urequests.post(URL_CLOUD, data=payload_txt, headers=headers)
#         status = response.status_code
#         response.close()
        
#         # Si Google répond 200 ou 201, l'envoi est validé
#         return status in (200, 201)
#     except:
#         return False

# # Variables de chronométrage
# last_send = time.ticks_ms()
# wifi_tx_success = False

# # --- 4. BOUCLE PRINCIPALE ---
# while True:
#     now = time.ticks_ms()
    
#     # On vérifie l'état du Wi-Fi en tâche de fond pour chaque cycle
#     wifi_actif = wlan.isconnected()
    
#     # Lecture du GPS (Port C / Bleu)
#     fix = sensor.read_gps(timeout_ms=500)
    
#     if fix:
#         lat, lon, spd = fix
#         if spd < 5.0: 
#             spd = 0.0
        
#         # Tentative d'envoi toutes les 10 secondes
#         if time.ticks_diff(now, last_send) >= 10000:
#             if wifi_actif:
#                 wifi_tx_success = send_via_wifi(lat, lon, spd, 1)
#             else:
#                 # Si le Wi-Fi a coupé, on tente une reconnexion flash
#                 wifi_actif = gerer_connexion_wifi()
#                 wifi_tx_success = False
#             last_send = time.ticks_ms()
        
#         # MISE À JOUR ÉCRAN : Le dernier paramètre contrôle le voyant TX (Vert si True)
#         # Ici, le voyant passe au VERT si l'envoi Wi-Fi a réussi
#         ui_interface.update_display(spd, lat, lon, True, wifi_tx_success)
        
#     else:
#         # SIMULATION / REPLI : Même si le GPS cherche le signal à cause des arbres ou des bâtiments,
#         # on veut quand même tester notre Wi-Fi ! On force un envoi fictif toutes les 10 secondes.
#         if time.ticks_diff(now, last_send) >= 10000:
#             if wifi_actif:
#                 # On envoie des coordonnées de test (Ex: HEC Lausanne) pour valider le Cloud
#                 wifi_tx_success = send_via_wifi(46.5234, 6.5845, 0.0, 1)
#             else:
#                 gerer_connexion_wifi()
#                 wifi_tx_success = False
#             last_send = time.ticks_ms()
            
#         # L'écran affiche 0.0 mais le voyant passera au VERT si le message fictif est bien arrivé sur Google Cloud
#         ui_interface.update_display(0.0, 0.0, 0.0, False, wifi_tx_success)
        
#     time.sleep_ms(200)
