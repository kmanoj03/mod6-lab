import json
import os
import time
import urllib.request
from datetime import datetime

URL = os.environ.get("INVENTORY_URL", "http://inventory-service:8080/items")
INTERVAL = float(os.environ.get("INTERVAL_SECONDS", "1"))

print(f"Client sending requests to {URL}", flush=True)
while True:
    ts = datetime.now().strftime("%H:%M:%S")
    try:
        with urllib.request.urlopen(URL, timeout=2) as resp:
            body = json.loads(resp.read())
            print(f"{ts} OK  served-by={body['pod']} ip={body['podIP']} items={len(body['items'])}", flush=True)
    except Exception as exc:
        print(f"{ts} ERR {exc}", flush=True)
    time.sleep(INTERVAL)
