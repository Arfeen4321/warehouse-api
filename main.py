import os
import time
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Warehouse Management API", version="1.0.0")

IS_READY = True
IS_ALIVE = True

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['endpoint'])

inventory_db = [
    {"id": 1, "sku": "WIDGET-001", "name": "Standard Industrial Widget", "quantity": 150, "location": "Aisle-3-Shelf-B"},
    {"id": 2, "sku": "PALLET-404", "name": "Heavy Duty Wooden Pallet", "quantity": 45, "location": "Zone-C"}
]

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status_code=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
    return response

@app.get("/")
def read_root():
    return {"service": "warehouse-api", "version": "1.0.0", "environment": os.getenv("ENVIRONMENT", "development")}

@app.get("/healthz")
def liveness_probe(response: Response):
    if not IS_ALIVE:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "unhealthy"}
    return {"status": "alive"}

@app.get("/readyz")
def readiness_probe(response: Response):
    if not IS_READY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not_ready"}
    return {"status": "ready"}

@app.get("/api/v1/inventory")
def get_inventory():
    return {"count": len(inventory_db), "items": inventory_db}

@app.get("/metrics")
def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
