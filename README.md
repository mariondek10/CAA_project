# CAA Bike Tracker Project 🚲

An end-to-end IoT tracking solution that collects GPS data during cycling sessions, processes it on an ESP32-based microcontroller, and visualizes it via a cloud-deployed dashboard.

## Overall Architecture

The hardware logic relies on parsing NMEA data from the GPS module and sending smoothed telemetry over Wi-Fi.

**Hardware Flow:**
`GPS Module (9600 baud)` ──> `Grove HUB` ──> `Port C (UART2)` ──> `M5Stack Core2`

## M5Stack Functionalities

The M5Stack acts as the edge device, handling data collection, processing, and session management.

- **Smart Wi-Fi Configuration:** On boot, the device enters an interactive Wi-Fi configuration mode. If ignored, it automatically connects to the default pre-configured network.
- **Manual Session Management:** The GPS searches for a fix automatically, but data recording only begins upon user action.
  - **Button A (Left):** Start session / Pause session / Resume session.
  - **Button C (Right):** Stop & save session (forces a buffer flush). Pressing Start again generates a new session ID.
- **Data Smoothing:** Raw GPS speeds `< 2.0 km/h` are filtered out. The display uses a Simple Moving Average (SMA) of the last 2 readings to prevent erratic speed jumps.
- **Custom speed zones:** The UI displays real-time animal icons based on the rider's pace:
  - 🐢 **Tortoise:** < 15 km/h
  - 🐰 **Bunny:** 15 - 25 km/h
  - 🦁 **Lion:** > 25 km/h

## Cloud & dashboard implementation

The backend architecture ensures reliable data ingestion and provides an analytical hub.

- **Database:** Google BigQuery (`geo_data` table).
- **Backend:** A Flask application containerized with Docker and deployed on **Google Cloud Run**. The endpoint validates incoming payloads via a hashed password before inserting records into BigQuery.
- **Frontend:** A Streamlit dashboard utilizing Plotly Express for route mapping and pandas for pace analysis.
- **Security:** API keys and credentials are securely managed via Google Cloud Secret Manager.

**Live Backend Endpoint:** `https://bike-backend-387007830650.europe-west6.run.app/send-to-bigquery`
