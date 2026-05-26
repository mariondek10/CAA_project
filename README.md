# CAA Bike Tracker Project 🚲

An end-to-end IoT tracking solution that collects GPS data during cycling sessions, processes it on an ESP32-based microcontroller, and visualizes it via a cloud-deployed dashboard.

## Members of the group

- Marine Hosch
- Marion de Kerchove

### Workload distribution:

Overall, we both worked on all aspects of the project, either collaborating directly or building on each other’s work. Although we both contributed to the project as a whole, Marion focused particularly on the Google Cloud, backend and dashboard aspects, whilst Marine mainly worked on the features related to the M5Stack.

## Overall architecture

The hardware logic relies on parsing NMEA data from the GPS module and sending smoothed telemetry over Wi-Fi.

**Hardware Flow:**
`GPS Module (9600 baud)` ──> `Grove HUB` ──> `Port C (UART2)` ──> `M5Stack Core2`

## M5Stack Functionalities

The M5Stack acts as the edge device, handling data collection, processing, and session management.

- **Smart Wi-Fi Configuration:** On boot, the device enters an interactive Wi-Fi configuration mode. If ignored, it automatically connects to the default pre-configured network.
- **Manual Session Management:** The GPS searches for a fix automatically, but data recording only begins upon user action.
  - **Button A (Left):** Start session / Pause session / Resume session.
  - **Button C (Right):** Stop & save session (forces a buffer flush). Pressing Start again generates a new session ID.
- **Data Smoothing:** Raw GPS speeds `< 2.0 km/h` are filtered out. The display uses a Simple Moving Average (SMA) of the last 3 readings to prevent erratic speed jumps.
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

## Deployement guide

To replicate this project locally or deploy it to your own Google Cloud Platform (GCP) instance, follow these steps:

### 1. Database setup (Google BigQuery)

Create a DB named `BikeProject` with a table `geo_data` as follow :

```sql
CREATE TABLE `caabikeproject.BikeProject.geo_data` (
    latitude FLOAT64,
    longitude FLOAT64,
    speed FLOAT64,
    session_id INT64,
    timestamp TIMESTAMP
);
```

### 2. Backend

The backend functions are dockerized container deployed on Google Cloud
to build and deploy, in your terminal, navigate to the backend directory and run the following command:

```bash
# Build app (make sure d'avoir pull et d'etre dans le directory /dashboard)
gcloud builds submit --tag europe-west6-docker.pkg.dev/caabikeproject/bike-repo/bike_app:latest .

# Run app
gcloud run deploy bike-app   --image europe-west6-docker.pkg.dev/caabikeproject/bike-repo/bike_app:latest   --region europe-west6   --allow-unauthenticated

# Build backend (make sure d'avoir pull et d'etre dans le directory /backend)
gcloud builds submit --tag europe-west6-docker.pkg.dev/caabikeproject/bike-repo/bike_backend:latest .

# Run backend
gcloud run deploy bike-backend   --image europe-west6-docker.pkg.dev/caabikeproject/bike-repo/bike_backend:latest   --region europe-west6   --allow-unauthenticated
```

### Frontend deployement (Streamlit)

To deploy and run the user dashboard locally, in your terminal, go to the dashboard directory ans run the following command:

```bash
pip install -r requirements.txt
streamlit run app.py
```

### M5stack

To run the m5stack dashboard on your device, upload the following files to the device :

- main.py
- sensor.py
- ui_interface.py
- boot.py

You can update the default Wifi configuration (WIFI_SSID, WIFI_PASS)in the boot.py file.

Update the flask URL (FLASK_URL) and Wifi configuration (WIFI_SSID, WIFI_PASS) in the main.py file.

## Links

**Live Backend Endpoint:** [Link](https://bike-backend-387007830650.europe-west6.run.app/send-to-bigquery)

**Live Dashboard of sessions:** [Link](https://bike-app-387007830650.europe-west6.run.app/)

**YouTube video:** [Link]()

**Github repository:\*** `[Link](https://github.com/mariondek10/CAA_project)

```

```
