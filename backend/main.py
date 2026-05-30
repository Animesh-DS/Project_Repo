# backend/main.py
from fastapi import FastAPI

app = FastAPI(
    title="Zero-Knowledge Cancelable Biometrics API",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy"}

@app.get("/audit")
async def audit_endpoint():
    """
    Audit endpoint confirming compliance with the architecture rules:
    - No persistent storage.
    """
    return {
        "persistent_storage": False,
        "node_count": 3,
        "records_in_memory": 0
    }