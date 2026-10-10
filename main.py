import os, time
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Warehouse Management API", version="3.0.0")

inventory_db = [
    {"id": 1, "sku": "WIDGET-001", "name": "Standard Industrial Widget", "quantity": 150, "location": "Aisle-3-Shelf-B"},
    {"id": 2, "sku": "PALLET-404", "name": "Heavy Duty Wooden Pallet", "quantity": 45, "location": "Zone-C"},
    {"id": 3, "sku": "FORKLIFT-99", "name": "Heavy Electric Forklift 3000KG", "quantity": 5, "location": "Bay-A"},
    {"id": 4, "sku": "ROBOT-ARM-500", "name": "Automated Robotic Sorting Arm AI", "quantity": 12, "location": "Tech-Lab-2"}
]

@app.get("/")
def read_root(): return {"service": "warehouse-api", "version": "3.0.0", "status": "running"}

@app.get("/healthz")
def liveness_probe(): return {"status": "alive"}

@app.get("/readyz")
def readiness_probe(): return {"status": "ready"}

@app.get("/api/v1/inventory")
def get_inventory(): return {"count": len(inventory_db), "release": "v3.0.0", "items": inventory_db}
