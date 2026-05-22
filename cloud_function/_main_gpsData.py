## Cloud Function to receive GPS data from m5stack and insert into BigQuery 

import base64
import struct
import functions_framework
from google.cloud import bigquery
from datetime import datetime
import json

client = bigquery.Client()
TABLE_ID = "caabikeproject.BikeProject.geo_data"

@functions_framework.http
def receive_gps(request):
    if request.method != 'POST':
        return 'Method not allowed', 405
    
    secret = request.headers.get('X-Secret-Key')
    if secret != 'BIKE_SECRET_2026':
        return 'Unauthorized', 401

    request_json = request.get_json(silent=True)
    if not request_json:
        return 'No data', 400

    try:
        if 'uplink_message' not in request_json:
            return 'Not a TTN uplink', 400
            
        payload_b64 = request_json['uplink_message'].get('frm_payload')
        if not payload_b64:
            return 'No payload', 400

        payload_bytes = base64.b64decode(payload_b64)
        
        # '<iiBB' = 4 octets (lat) + 4 octets (lon) + 1 octet (speed) + 1 octet (session)
        lat_int, lon_int, speed, session_id = struct.unpack('<iiBB', payload_bytes)
        
        row = {
            "latitude": lat_int / 100000.0,
            "longitude": lon_int / 100000.0,
            "speed": float(speed),
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": int(session_id)
        }

        print(f"Insertion BQ : {row}") 

        errors = client.insert_rows_json(TABLE_ID, [row])
        if errors:
            print(f"Erreur BigQuery : {errors}")
            return json.dumps({"error": str(errors)}), 500
        
        return json.dumps({"status": "ok"}), 200

    except Exception as e:
        print(f"Erreur serveur : {e}")
        return json.dumps({"error": str(e)}), 500