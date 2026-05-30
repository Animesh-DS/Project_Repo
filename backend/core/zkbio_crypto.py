import hashlib
import hmac
from .fuzzy_extractor import generate_sketch, reproduce_sketch

def generate(bio_bits: bytes) -> tuple[bytes, bytes]:
   
    seed, helper_data = generate_sketch(bio_bits)
    stable_key = hashlib.sha256(seed).digest()
    return stable_key, helper_data

def reproduce(bio_bits: bytes, helper_data: bytes) -> bytes:
    seed = reproduce_sketch(bio_bits, helper_data)
    stable_key = hashlib.sha256(seed).digest()
    return stable_key

def commit(stable_key: bytes) -> str:
    return hashlib.sha256(stable_key).hexdigest()

def verify_commitment(stable_key: bytes, commitment_hex: str) -> bool:
    return hmac.compare_digest(commit(stable_key).encode('utf-8'), commitment_hex.encode('utf-8'))