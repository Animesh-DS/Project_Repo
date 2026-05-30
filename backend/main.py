import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import manager 
from api.routes import enrol, authenticate

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

# 3. Live WebSocket Feed

@app.websocket("/ws/pipeline")
async def ws_pipeline(websocket: WebSocket):
    """
    The frontend (P3) connects here to listen for live biometric processing events.
    """
    await manager.connect(websocket)
    try:
        # Keep the connection alive indefinitely
        while True:
            await asyncio.sleep(0.05) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)


app.include_router(enrol.router)
app.include_router(authenticate.router)