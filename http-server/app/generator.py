import random
from datetime import datetime, timezone

DEVICE_IDS = ["pdu-01", "pdu-02", "pdu-03"]

def generate_metrics():
    metrics = []
    for device_id in DEVICE_IDS:
        metrics.append({
            "device_id": device_id,
            "voltage": round(random.uniform(220, 240), 1),
            "current": round(random.uniform(0.8, 2.0), 2),
            "temperature": round(random.uniform(28.0, 40.0), 1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
    return metrics
