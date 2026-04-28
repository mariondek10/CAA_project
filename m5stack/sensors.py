from machine import UART
import time
uart = UART(2, baudrate=115200, rx=16, tx=17)
time.sleep_ms(200)

for cmd in ['AT+DEVEUI?', 'AT+APPEUI?', 'AT+APPKEY?']:
uart.write((cmd + '\r\n').encode())
time.sleep_ms(500)
resp = uart.read() if uart.any() else b'no response'
print(f"{cmd} → {resp.decode('utf-8', 'ignore').strip()}")

uart.deinit()