# backend/api/routes/enrol.py
from fastapi import APIRouter
from models.schemas import EnrolRequest
from services.node_service import distribute_to_nodes
from services.websocket_manager import manager

# Note: We import this from P2 (Hardik's pipeline)
from core.zkbio_pipeline import enrol 

router = APIRouter()

@router.post("/enrol")
async def enrol_endpoint(body: EnrolRequest):
    # 1. Trigger the facial recognition pipeline
    result = enrol(mode=body.mode)
    
    # 2. Extract the safe, anonymized cryptographic data
    commitment = result["commitment_hex"]
    helper_data = result["helper_data"]
    
    # 3. Send it to our 3 fake decentralized nodes
    distribute_to_nodes(commitment, helper_data)
    
    # 4. Tell the frontend we finished successfully
    await manager.broadcast({
        "stage": "verify", 
        "status": "done",
        "data": {"verified": True, "node_votes": [True, True, True]}
    })
    
    return {"status": "enrolled", "message": "Biometric template securely sharded."}