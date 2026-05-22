from hardware import sdcard
try:
    sdcard.SDCard(20000000)
except:
    pass

import network
import time

# Wi-Fi configuration
WIFI_SSID     = "iPhone (48)"
WIFI_PASSWORD = "09651234"

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        print("Deja connecte:", wlan.ifconfig()[0])
        return True

    print("Connexion au Wi-Fi...")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    
    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        
        print("  ..." + str(timeout) + "s")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("Connecte ! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("Echec connexion Wi-Fi")
        return False


connect_wifi()
