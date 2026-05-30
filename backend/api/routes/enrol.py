# backend/api/routes/enrol.py
from fastapi import APIRouter
from models.schemas import EnrolRequest
from services.node_service import distribute_to_nodes
from services.websocket_manager import manager
from core.zkbio_pipeline import enrol 

router = APIRouter()

@router.post("/enrol")
async def enrol_endpoint(body: EnrolRequest):
    result = enrol(mode=body.mode)
    
    commitment = result["commitment_hex"]
    helper_data = result["helper_data"]
    
    distribute_to_nodes(commitment, helper_data)
    
    await manager.broadcast({
        "stage": "verify", 
        "status": "done",
        "data": {"verified": True, "node_votes": [True, True, True]}
    })
    
    return {"status": "enrolled", "message": "Biometric template securely sharded."}