# backend/models/schemas.py
from pydantic import BaseModel
from typing import Literal

class EnrolRequest(BaseModel):
    mode: Literal["face", "fingerprint"] = "face"

class AuthRequest(BaseModel):
    mode: Literal["face", "fingerprint"] = "face"