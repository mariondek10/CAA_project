import libs.urequests as urequests
import ujson
import time

CLOUD_FUNCTION_URL = "https://function-retrieve-geo-data-387007830650.europe-west6.run.app/"
SECRET_KEY = "BIKE_SECRET_2026"

# Généré une fois au boot — identifie la sortie
SESSION_ID = "ride_{:010d}".format(time.time())
print("Session:", SESSION_ID)

def send_to_bigquery(lat, lon, speed):
    try:
        payload = ujson.dumps({
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "session_id": SESSION_ID
        }) 
        r = urequests.post(
            CLOUD_FUNCTION_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "X-Secret-Key": SECRET_KEY
            }
        )
        ok = r.status_code == 200
        print("BQ status:", r.status_code)
        r.close()
        return ok
    except Exception as e:
        print("BQ error:", e)
        return False