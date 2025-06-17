import requests
import random
import time
from datetime import datetime, timezone

url = "http://127.0.0.1:5000/receive"

while True:
    value = round(random.uniform(80, 250), 2)
    payload = {
        "location": "area1",
        "value": value,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    try:
        r = requests.post(url, json=payload)
        print("Sent:", payload, "Status:", r.status_code)
    except Exception as e:
        print("Error:", e)
    time.sleep(5)
