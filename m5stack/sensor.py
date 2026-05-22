from machine import UART
import time

TX_PIN = 14
RX_PIN = 13

## Parse the GNRMC sentence to extract latitude, longitude and speed
def parse_gnrmc(sentence):
    try:
        parts = sentence.strip().split(',')
        if len(parts) < 8 or parts[2] != 'A': 
            return None
        if not (parts[0] in ('$GNRMC', '$GPRMC')):
            return None
        
        lat = float(parts[3][:2]) + float(parts[3][2:]) / 60
        if parts[4] == 'S': lat = -lat
        
        lon = float(parts[5][:3]) + float(parts[5][3:]) / 60
        if parts[6] == 'W': lon = -lon
        
        
        speed_knots = float(parts[7]) if parts[7] else 0.0
        speed_kmh = speed_knots * 1.852 
        
        return lat, lon, speed_kmh 
    except:
        return None

## Read GPS data from the UART and parse it, with a timeout
def read_gps(timeout_ms=1000):
    uart = UART(2, baudrate=9600, tx=TX_PIN, rx=RX_PIN, timeout=500)
    fix = None
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            line = uart.readline()
            if line:
                try:
                    decoded = line.decode('utf-8', 'ignore').strip()
                    if 'RMC' in decoded:
                        fix = parse_gnrmc(decoded)
                        if fix:
                            break
                except:
                    pass
    uart.deinit()
    return fix


## Main loop to read GPS, check Wi-Fi and send data to backend, while updating the UI
def run_loop():
    print("Lancement GPS...")
    while True:
        try:
            fix = read_gps(timeout_ms=1000)
            if fix:
                lat, lon = fix
                print("GPS OK: {:.6f}, {:.6f}".format(lat, lon))
            else:
                print("En attente GPS...")
        except Exception as e:
            print("Erreur:", e)
        time.sleep_ms(500)
        


