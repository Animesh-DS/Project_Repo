# backend/api/routes/authenticate.py
from fastapi import APIRouter
from models.schemas import AuthRequest
from services.node_service import query_nodes
from services.websocket_manager import manager

from core.zkbio_pipeline import authenticate

router = APIRouter()

# Faking a mobile phone's secure storage for the demo
DEMO_PHONE_STORAGE = {
    "commitment_hex": "placeholder_hex",
    "helper_data": b"placeholder_bytes"
}

@router.post("/authenticate")
async def authenticate_endpoint(body: AuthRequest):
    # 1. Read the data from the "user's phone"
    stored_helper = DEMO_PHONE_STORAGE["helper_data"]
    stored_hex = DEMO_PHONE_STORAGE["commitment_hex"]
    
    # 2. Run Hardik's pipeline to process the new webcam image
    result = authenticate(stored_helper, stored_hex, mode=body.mode)
    candidate_hex = result["commitment_hex"]
    
    # 3. Ask the 3 decentralized nodes if they recognize this new hash
    node_votes = query_nodes(candidate_hex)
    
    # 4. Did at least 2 out of 3 nodes say yes? (Majority rule)
    verified = sum(node_votes) >= 2 
    
    # 5. Blast the final result to Ayushman's UI
    await manager.broadcast({
        "stage": "verify", 
        "status": "done",
        "data": { "verified": verified, "node_votes": node_votes }
    })
    
    return {"verified": verified, "node_votes": node_votes}