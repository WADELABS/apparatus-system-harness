from typing import Dict, Any, List
from src.triage import TriageEngine

class Orchestrator:
    """
    Coordinates the three-pillar Truth Substrate via deterministic triage.
    """
    def __init__(self):
        self.triage = TriageEngine()

    def run_diagnostic_trace(self, incident: str, telemetry: Dict[str, bool]) -> Dict[str, Any]:
        """
        Enforces a high-fidelity diagnostic trace (Apparatus -> System -> Harness).
        """
        incident_id = self.triage.log_incident(incident)
        
        # Sequentially verify layers
        result = self.triage.run_trace(incident_id, telemetry)
        
        return {
            "incident_id": incident_id,
            "trace_result": result,
            "can_actuate": result["status"] == "CLEARED"
        }

    def process_instruction(self, instruction: str) -> Dict[str, Any]:
        """Legacy support for instruction processing."""
        return {
            "instruction": instruction,
            "status": "DEPRECATED",
            "message": "Use run_diagnostic_trace for forensic triage."
        }
