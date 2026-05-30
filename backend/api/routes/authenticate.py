# backend/api/routes/authenticate.py
import asyncio
from fastapi import APIRouter, HTTPException
from models.schemas import AuthRequest
from services.node_service import query_nodes
from services.websocket_manager import manager
from services.mock_phone import DEMO_PHONE_STORAGE
from core.zkbio_pipeline import authenticate

router = APIRouter()

@router.post("/authenticate")
async def authenticate_endpoint(body: AuthRequest):
    try:
        stored_helper = DEMO_PHONE_STORAGE.get("helper_data")
        stored_hex = DEMO_PHONE_STORAGE.get("commitment_hex")

        if stored_helper is None or stored_hex is None:
            raise HTTPException(status_code=400, detail="No biometric data found on device. Please enrol first.")
        
        result = await asyncio.to_thread(
            authenticate, 
            stored_helper, 
            stored_hex, 
            mode=body.mode
        )
        
        candidate_hex = result["commitment_hex"]
        node_votes = query_nodes(candidate_hex)
        verified = sum(node_votes) >= 2 
        
        await manager.broadcast({
            "stage": "verify", 
            "status": "done",
            "data": { "verified": verified, "node_votes": node_votes }
        })
        
        if not verified:
            raise HTTPException(status_code=401, detail="Biometric authentication failed. Identity not verified.")
            
        return {"verified": verified, "node_votes": node_votes}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Authentication Pipeline Error: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Biometric processing error: {str(e)}"
        )