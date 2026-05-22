#%%
from flask import Flask, request
import os
from google.cloud import bigquery
import requests
from datetime import datetime
import json
from google.cloud import secretmanager
from google.oauth2 import service_account

#key_path = r"C:\Users\marin\bike_project\caabikeproject-ee4a905a2516.json"

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

def get_bigquery_client():
    sm = secretmanager.SecretManagerServiceClient()
    # Utilise ton vrai nom de secret et ton project number
    name = "projects/387007830650/secrets/key-bikeProject/versions/latest"
    response = sm.access_secret_version(request={"name": name})
    key_dict = json.loads(response.payload.data.decode("UTF-8"))
    
    credentials = service_account.Credentials.from_service_account_info(key_dict)
    return bigquery.Client(project="caabikeproject", credentials=credentials)

client = get_bigquery_client()

PROJECT_NAME = "caabikeproject"


# For authentication

YOUR_HASH_PASSWD = "M&M's" # YOUR_HASH_PASSWD

app = Flask(__name__)

# get the column names of the db
q = """
SELECT * FROM `caabikeproject.BikeProject.geo_data` LIMIT 10
"""
query_job = client.query(q)
df = query_job.to_dataframe()
#%%

@app.route('/send-to-bigquery', methods=['GET', 'POST'])
def send_to_bigquery():
    if request.method == 'POST':
        body = request.get_json(force=True)
        
        if body["passwd"] != YOUR_HASH_PASSWD:
            return {"status": "failed", "reason": "Incorrect Password!"}, 401
        
        data = body["values"]
        # Champs FLOAT dans geo_data
        float_fields = {"latitude", "longitude", "speed"}
        data["timestamp"] = datetime.utcnow().isoformat()

        names = ", ".join(data.keys())
        values_parts = []
        for k, v in data.items():
            if k in float_fields:
                values_parts.append(str(float(v)))
            elif k == "session_id":
                values_parts.append(str(int(v)))
            else:
                # Si c'est le timestamp, on ajoute le mot-clé TIMESTAMP pour BigQuery
                if k == "timestamp":
                    values_parts.append(f"TIMESTAMP('{v}')")
                else:
                    # Pour les autres strings classiques s'il y en a
                    values_parts.append(f"'{v}'")
        values = ", ".join(values_parts)
                

        q = f"INSERT INTO `caabikeproject.BikeProject.geo_data` ({names}) VALUES ({values})"
        client.query(q)
        return {"status": "success", "data": data}
    
    return {"status": "failed"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)