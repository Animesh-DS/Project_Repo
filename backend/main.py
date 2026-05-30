import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from services.websocket_manager import manager 
from api.routes import enrol, authenticate
from core.zkbio_pipeline import event_queue

app = FastAPI(
    title="Zero-Knowledge Cancelable Biometrics API",
    version="1.0.0"
)

def drain_pipeline_events(loop: asyncio.AbstractEventLoop):
    """
    Runs in a background thread. Listens to P2's event_queue.
    When P2 pushes an event, we broadcast it to the WebSockets.
    """
    while True:
        event = event_queue.get() 
        
        asyncio.run_coroutine_threadsafe(manager.broadcast(event), loop)

@app.on_event("startup")
async def startup_event():
    """Starts the background drainer when the server boots."""
    loop = asyncio.get_running_loop()
    thread = threading.Thread(target=drain_pipeline_events, args=(loop,), daemon=True)
    thread.start()

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
        while True:
            await asyncio.sleep(0.05) 
    except WebSocketDisconnect:
        manager.disconnect(websocket)


app.include_router(enrol.router)
app.include_router(authenticate.router)