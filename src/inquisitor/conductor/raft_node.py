from pysyncobj import SyncObj, replicated
import logging
from typing import Dict, Any, List
import uuid

class InquisitorConductor(SyncObj):
    """
    Layer 1: High Availability Conductor.
    Uses Raft consensus to manage the state of financial market data inquiries.
    """
    
    def __init__(self, self_addr: str, partner_addrs: List[str]):
        super(InquisitorConductor, self).__init__(self_addr, partner_addrs)
        self.__manifest_registry = {}
        self.__active_inquiries = {}
        logging.info(f"Conductor initialized on {self_addr}")

    @replicated
    def submit_manifest(self, manifest_id: str, manifest_data: Dict[str, Any]):
        """Replicated method to submit a new inquiry manifest."""
        self.__manifest_registry[manifest_id] = {
            "data": manifest_data,
            "status": "PENDING",
            "submitted_at": uuid.uuid4().hex # Simplified timestamp
        }
        logging.info(f"Manifest {manifest_id} replicated across cluster.")

    @replicated
    def update_inquiry_status(self, inquiry_id: str, status: str):
        """Update the status of an active inquiry."""
        self.__active_inquiries[inquiry_id] = status
        logging.info(f"Inquiry {inquiry_id} status updated to {status}")

    def get_manifests(self):
        return self.__manifest_registry

    def is_leader(self):
        """Check if this node is the Raft leader."""
        return self._getLeader() == self._SyncObj__selfAddr

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Demo use:
    # conductor = InquisitorConductor('localhost:1234', [])
