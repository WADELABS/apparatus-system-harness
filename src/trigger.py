"""
src/trigger.py
The Trigger Layer: Automating the transition from Void Detection to Apparatus Action.
"""

from typing import Dict, Any, Optional
from .orchestrator import Orchestrator
from ..WADELABS_API import SignalType, WadelabsSignal

class TriggerLayer:
    """
    The automated 'Trigger' that bridges the 'Harness Gap'.
    It listens for signals and automatically initiates the Inquisitor's Gauntlet.
    """
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def handle_signal(self, signal: WadelabsSignal) -> Optional[Dict[str, Any]]:
        """
        Receives a signal and triggers the appropriate ASH manifestation.
        """
        print(f"DEBUG: ASH Trigger Layer received signal: {signal.signal_type.value}")
        
        if signal.signal_type == SignalType.VOID_DETECTED:
            return await self._trigger_void_inquiry(signal.payload)
        
        return None

    async def _trigger_void_inquiry(self, mapped_void: Dict[str, Any]) -> Dict[str, Any]:
        """
        Automatically bridges a Negative Space void to an ASH Inquiry.
        """
        print(f"⚙️ [ASH TRIGGER]: Automated bridge activated for void in '{mapped_void.get('claim', 'unknown')}'")
        
        # Prepare the Inquiry Manifest
        inquiry_manifest = {
            "id": f"INQ-{int(time.time())}",
            "origin": "NEGATIVE_SPACE_VOID",
            "target_layer": mapped_void.get("target_layer", "SYSTEM"),
            "payload": mapped_void
        }
        
        # ACTIVATE THE INQUISITOR
        return await self.orchestrator.orchestrate_cognitive_stack(inquiry_manifest)

import time
