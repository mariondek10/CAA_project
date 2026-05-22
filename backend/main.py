#%%
from flask import Flask, request
import os
from google.cloud import bigquery
import requests
from datetime import datetime

key_path = r"C:\Users\marin\bike_project\caabikeproject-ee4a905a2516.json"

# You only need to uncomment the line below if you want to run your flask app locally.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
client = bigquery.Client(project="caabikeproject")

#%%

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