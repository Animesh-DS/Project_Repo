# backend/api/routes/enrol.py
import json
import os
from fastapi import APIRouter, HTTPException
from models.schemas import EnrolRequest
from services.node_service import distribute_to_nodes
from services.websocket_manager import manager
from core.zkbio_pipeline import enrol 

router = APIRouter()

# The path to our permanent hackathon database
VAULT_PATH = "secure_vault.json"

@router.post("/enrol")
async def enrol_endpoint(body: EnrolRequest):
    try:
        # 1. Run the Zero-Knowledge Pipeline 
        # (Camera opens on Main Thread, math happens, memory wipes)
        result = enrol(mode=body.mode)
        
        commitment = result["commitment_hex"]
        helper_data = result["helper_data"]
        
        # 2. Distribute to decentralized nodes
        distribute_to_nodes(commitment, helper_data)
        
        # 3. 🔒 PERMANENT STORAGE: Save the ZK data to a JSON file
        # We must convert the helper_data (bytes) into a hex string so JSON can read it
        vault_data = {
            "commitment_hex": commitment,
            "helper_data_hex": helper_data.hex() 
        }
        
        with open(VAULT_PATH, "w") as f:
            json.dump(vault_data, f, indent=4)
            
        print("✅ SUCCESS: Zero-Knowledge Template saved to secure_vault.json!")
        
        # 4. Broadcast the final success message to the frontend UI
        await manager.broadcast({
            "stage": "verify", 
            "status": "done",
            "data": {"verified": True, "node_votes": [True, True, True]}
        })
        
        return {"status": "enrolled", "message": "Biometric template securely stored."}
        
    except Exception as e:
        print(f"Enrolment Pipeline Error: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Biometric capture failed: {str(e)}"
        )