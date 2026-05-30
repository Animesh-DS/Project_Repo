# backend/api/routes/authenticate.py
from fastapi import APIRouter
from models.schemas import AuthRequest
from services.node_service import query_nodes
from services.websocket_manager import manager
from services.mock_phone import DEMO_PHONE_STORAGE
from core.zkbio_pipeline import authenticate

router = APIRouter()

DEMO_PHONE_STORAGE = {
    "commitment_hex": "placeholder_hex",
    "helper_data": b"placeholder_bytes"
}

@router.post("/authenticate")
async def authenticate_endpoint(body: AuthRequest):
    stored_helper = DEMO_PHONE_STORAGE["helper_data"]
    stored_hex = DEMO_PHONE_STORAGE["commitment_hex"]

    if stored_helper is None or stored_hex is None:
            raise HTTPException(status_code=400, detail="No biometric data found on device. Please enrol first.")
    
    result = authenticate(stored_helper, stored_hex, mode=body.mode)
    candidate_hex = result["commitment_hex"]
    
    node_votes = query_nodes(candidate_hex)
    
    verified = sum(node_votes) >= 2 
    
    await manager.broadcast({
        "stage": "verify", 
        "status": "done",
        "data": { "verified": verified, "node_votes": node_votes }
    })
    
    return {"verified": verified, "node_votes": node_votes}