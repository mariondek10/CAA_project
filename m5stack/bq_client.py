import libs.urequests as urequests
import ujson

CLOUD_FUNCTION_URL = "REMPLACE_PAR_URL_APRES_DEPLOY"
SECRET_KEY = "TO_SET"

def send_to_bigquery(lat, lon, speed):
    try:
        payload = ujson.dumps({
            "lat": lat,
            "lon": lon,
            "speed": speed
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
        r.close()
        return ok
    except Exception as e:
        print("BQ error:", e)
        return False