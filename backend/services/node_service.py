# backend/services/node_service.py
import hashlib

class MockNode:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self._store: dict[str, str] = {}

    def store(self, commitment_hex: str, helper_data: bytes) -> None:
        helper_data_hash = hashlib.sha256(helper_data).hexdigest()
        self._store[commitment_hex] = helper_data_hash

    def query(self, candidate_hex: str) -> bool:
        return candidate_hex in self._store
        
    def count_records(self) -> int:
        return len(self._store)

# The "Network" - Spin up exactly 3 nodes
nodes = [MockNode(1), MockNode(2), MockNode(3)]

def distribute_to_nodes(commitment_hex: str, helper_data: bytes) -> None:
    """Simulates sending the enrollment data to all 3 independent nodes."""
    for node in nodes:
        node.store(commitment_hex, helper_data)

def query_nodes(candidate_hex: str) -> list[bool]:
    """Asks all 3 nodes if they recognize this commitment. Returns e.g. [True, True, True]"""
    return [node.query(candidate_hex) for node in nodes]

def get_total_records_in_memory() -> int:
    """Helper for the /audit endpoint to prove we aren't using a real database."""
    return nodes[0].count_records()