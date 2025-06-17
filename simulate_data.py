import requests
import random
import time
from datetime import datetime, timezone

# 🔁 REPLACE this with your actual Railway URL if needed
URL = "https://sensor-dashboard.up.railway.app/receive"

def generate_sensor_data():
    return {
        "location": "area1",
        "value": round(random.uniform(80, 250), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

while True:
    data = generate_sensor_data()
    try:
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            print(f"[✔] Sent: {data}")
        else:
            print(f"[✘] Failed to send | Status: {response.status_code} | Data: {data}")
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
    
    time.sleep(5)  # Wait 5 seconds before sending the next reading
