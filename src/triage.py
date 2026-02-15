"""
src/triage.py
Triage Logic: State machine for layer-by-layer diagnostics.
"""

from typing import Dict, List, Optional
from enum import Enum, auto

class TriageLayer(Enum):
    APPARATUS = auto()
    SYSTEM = auto()
    HARNESS = auto()
    RESOLVED = auto()

class TriageState:
    def __init__(self, incident: str):
        self.incident = incident
        self.current_layer = TriageLayer.APPARATUS
        self.findings = []
        self.is_cleared = False

    def report_finding(self, layer: TriageLayer, issue: str, resolved: bool = False):
        self.findings.append({"layer": layer.name, "issue": issue, "resolved": resolved})
        if resolved:
            self.advance_layer()

    def advance_layer(self):
        if self.current_layer == TriageLayer.APPARATUS:
            self.current_layer = TriageLayer.SYSTEM
        elif self.current_layer == TriageLayer.SYSTEM:
            self.current_layer = TriageLayer.HARNESS
        elif self.current_layer == TriageLayer.HARNESS:
            self.current_layer = TriageLayer.RESOLVED
            self.is_cleared = True

class TriageEngine:
    """
    Enforces a 'No-Skip' policy for diagnostics.
    """
    def __init__(self):
        self.incidents = {}

    def log_incident(self, incident: str) -> str:
        incident_id = str(hash(incident))
        self.incidents[incident_id] = TriageState(incident)
        return incident_id

    def run_trace(self, incident_id: str, checks: Dict[str, bool]) -> Dict:
        state = self.incidents.get(incident_id)
        if not state:
            return {"error": "Incident not found."}

        # Apparatus Layer
        if state.current_layer == TriageLayer.APPARATUS:
            if checks.get("physical_integrity", False):
                state.report_finding(TriageLayer.APPARATUS, "Hardware Clear", True)
            else:
                return {"status": "BLOCKED", "layer": "APPARATUS", "message": "Verify physical integrity before proceeding."}

        # System Layer
        if state.current_layer == TriageLayer.SYSTEM:
            if checks.get("logical_consistency", False):
                state.report_finding(TriageLayer.SYSTEM, "Commands Verified", True)
            else:
                return {"status": "BLOCKED", "layer": "SYSTEM", "message": "Verify logical commands before proceeding."}

        # Harness Layer
        if state.current_layer == TriageLayer.HARNESS:
            if checks.get("environmental_alignment", False):
                state.report_finding(TriageLayer.HARNESS, "Schedule/Context Valid", True)
            else:
                return {"status": "BLOCKED", "layer": "HARNESS", "message": "Verify operational context before proceeding."}

        return {
            "status": "CLEARED" if state.is_cleared else "IN_PROGRESS",
            "current_layer": state.current_layer.name,
            "findings": state.findings
        }
