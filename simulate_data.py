import requests
import random
import time
from datetime import datetime, timezone

URL = "https://sensor-dashboard.up.railway.app/receive"  # Replace with your actual URL

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
        print(f"Sent: {data} | Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send: {e}")
    
    time.sleep(5)
