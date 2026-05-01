# CAA_project

Overall Architecture
GPS (9600 baud) ──┐
├── Grove HUB ── Port C (UART2) ── M5Stack Core2
LoRa (115200) ──┘
Loop logic:
Switch to GPS baud → read NMEA → parse coordinates → calculate speed
Switch to LoRa baud → send payload to gateway → gateway forwards to BigQuery
