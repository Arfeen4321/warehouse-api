import os
from fastapi import FastAPI

app = FastAPI(title="Warehouse Management API", version="5.0.0")

inventory_db = [
    {"id": 1, "sku": "WIDGET-001", "name": "Standard Industrial Widget", "quantity": 150, "location": "Aisle-3-Shelf-B"},
    {"id": 2, "sku": "PALLET-404", "name": "Heavy Duty Wooden Pallet", "quantity": 45, "location": "Zone-C"},
    {"id": 3, "sku": "FORKLIFT-99", "name": "Heavy Electric Forklift 3000KG", "quantity": 5, "location": "Bay-A"},
    {"id": 4, "sku": "ROBOT-ARM-500", "name": "Automated Robotic Sorting Arm AI", "quantity": 12, "location": "Tech-Lab-2"},
    {"id": 5, "sku": "DRONE-DELIVERY-100", "name": "Autonomous Indoor Flight Delivery Drone", "quantity": 8, "location": "Roof-Pad-1"}
]

@app.get("/")
def read_root(): return {"service": "warehouse-api", "version": "5.0.0", "status": "running"}

@app.get("/healthz")
def liveness_probe(): return {"status": "alive"}

@app.get("/readyz")
def readiness_probe(): return {"status": "ready"}

@app.get("/api/v1/inventory")
def get_inventory(): return {"count": len(inventory_db), "release": "v5.0.0", "items": inventory_db}
# Testing Webhook Automation at Wed Oct 14 21:32:33 UTC 2026
# Live Webhook Verification Wed Oct 14 21:37:17 UTC 2026
# Webhook Live Trigger Test Wed Oct 14 21:44:30 UTC 2026
# Production Webhook Verified Wed Oct 14 21:47:34 UTC 2026
# Production Webhook Verified Wed Oct 14 21:51:34 UTC 2026
