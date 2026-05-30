# backend/api/routes/enrol.py
import asyncio
from fastapi import APIRouter, HTTPException
from models.schemas import EnrolRequest
from services.node_service import distribute_to_nodes
from services.websocket_manager import manager
from core.zkbio_pipeline import enrol 
from services.mock_phone import DEMO_PHONE_STORAGE  

router = APIRouter()

@router.post("/enrol")
async def enrol_endpoint(body: EnrolRequest):
    try:
        result = await asyncio.to_thread(enrol, mode=body.mode)
        
        commitment = result["commitment_hex"]
        helper_data = result["helper_data"]
        
        distribute_to_nodes(commitment, helper_data)
        
        DEMO_PHONE_STORAGE["commitment_hex"] = commitment
        DEMO_PHONE_STORAGE["helper_data"] = helper_data
        
        await manager.broadcast({
            "stage": "verify", 
            "status": "done",
            "data": {"verified": True, "node_votes": [True, True, True]}
        })
        
        return {"status": "enrolled", "message": "Biometric template securely sharded."}
        
    except Exception as e:
        print(f"Enrolment Pipeline Error: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Biometric capture failed: {str(e)}"
        )