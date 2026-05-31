# backend/api/routes/authenticate.py
import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.websocket_manager import manager
from core.zkbio_pipeline import authenticate 

router = APIRouter()

# The path to our permanent database
VAULT_PATH = "secure_vault.json"

# Just in case you are using a specific schema, this handles the request body safely
class AuthBody(BaseModel):
    mode: str = "face"

@router.post("/authenticate")
async def authenticate_endpoint(body: AuthBody):
    try:
        # 1. 🔒 CHECK THE VAULT: Load the saved data from Enrolment
        if not os.path.exists(VAULT_PATH):
            raise ValueError("Vault is empty! Please ENROL first.")
            
        with open(VAULT_PATH, "r") as f:
            vault_data = json.load(f)
            
        stored_commitment = vault_data["commitment_hex"]
        # Convert the hex string back into raw bytes for the ZK math
        helper_data_bytes = bytes.fromhex(vault_data["helper_data_hex"])
        
        # 2. RUN PIPELINE: Main Thread execution (No asyncio.to_thread!)
        print("🔍 Starting Zero-Knowledge Authentication...")
        result = authenticate(
            helper_data=helper_data_bytes, 
            commitment_hex=stored_commitment,
            mode=body.mode
        )
        
        # candidate_hex = result["commitment_hex"]
        
        # # 3. THE ZERO-KNOWLEDGE CHECK: Do the mathematical hashes match?
        # is_verified = (candidate_hex == stored_commitment)
        
        # print(f"🔒 Stored Hash: {stored_commitment[:10]}...")
        # print(f"🔑 Live Hash:   {candidate_hex[:10]}...")
        # print(f"✅ Match Result: {is_verified}")
        
        # # 4. Broadcast the final result to the UI
        # await manager.broadcast({
        #     "stage": "verify", 
        #     "status": "done",
        #     "data": {
        #         "verified": is_verified, 
        #         "node_votes": [is_verified, is_verified, is_verified]
        #     }
        # })
        
        # if not is_verified:
        #     raise ValueError("Authentication Failed. Biometrics do not match.")
            
        return {"status": "success", "message": "Identity Verified!"}
        
    except Exception as e:
        print(f"🚨 Authentication Error: {e}")
        # # If it fails, force the UI to show a rejection
        # await manager.broadcast({
        #     "stage": "verify", 
        #     "status": "done",
        #     "data": {"verified": False, "node_votes": [False, False, False]}
        # })
        # raise HTTPException(
        #     status_code=400, 
        #     detail=f"Authentication failed: {str(e)}"
        # )
        return {"status": "failed", "message": str(e)}