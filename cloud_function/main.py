import functions_framework
from google.cloud import bigquery
from datetime import datetime
import json

client = bigquery.Client()
TABLE_ID = "caabikeproject.BikeProject.geo-data"

@functions_framework.http
def receive_gps(request):
    if request.method != 'POST':
        return 'Method not allowed', 405
    
    # Clé secrète simple pour sécuriser l'endpoint
    secret = request.headers.get('X-Secret-Key')
    if secret != 'BIKE_SECRET_2026':
        return 'Unauthorized', 401

    data = request.get_json()
    if not data:
        return 'No data', 400

    row = {
        "latitude":  float(data['lat']),
        "longitude": float(data['lon']),
        "speed":     float(data['speed']),
        "timestamp": datetime.utcnow().isoformat()
    }

    errors = client.insert_rows_json(TABLE_ID, [row])
    if errors:
        return json.dumps({"error": str(errors)}), 500
    
    return json.dumps({"status": "ok"}), 200