# backend/services/node_service.py
import hashlib

class MockNode:
    def __init__(self, node_id: int):
        self.node_id = node_id
        # In-memory dictionary: Maps commitment_hex -> hash of helper_data
        # Note: If the server restarts, this gets wiped completely (Intentional for zero-knowledge!)
        self._store: dict[str, str] = {}

    def store(self, commitment_hex: str, helper_data: bytes) -> None:
        # STRICT RULE: NEVER store raw helper_data. Only store its SHA-256 hash.
        helper_data_hash = hashlib.sha256(helper_data).hexdigest()
        self._store[commitment_hex] = helper_data_hash

    def query(self, candidate_hex: str) -> bool:
        # Returns True if this node has this commitment saved
        return candidate_hex in self._store
        
    def count_records(self) -> int:
        # Useful for our /audit endpoint later
        return len(self._store)

