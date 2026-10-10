import os
from fastapi import FastAPI, Response, status

app = FastAPI(title="Warehouse Management API", version="2.0.1")

@app.get("/")
def read_root(): return {"service": "warehouse-api", "status": "bugged"}

# BUG: Liveness check returns 500 error!
@app.get("/healthz")
def liveness_probe(response: Response):
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"status": "unhealthy"}

@app.get("/readyz")
def readiness_probe(): return {"status": "ready"}
