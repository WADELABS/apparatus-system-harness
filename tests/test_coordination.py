"""
tests/test_coordination.py
Verification of the multi-pillar ASH orchestration flow.
"""

import unittest
from src.orchestrator import Orchestrator
from src.actuator import SystemActuator

class TestASHCoordination(unittest.TestCase):
    def setUp(self):
        self.orchestrator = Orchestrator()

    def test_layer_by_layer_triage_pass(self):
        """Test a full successful triage trace."""
        incident = "Lights turning on at 3 AM"
        
        # Step 1: Pass Apparatus
        telemetry = {"physical_integrity": True, "logical_consistency": True, "environmental_alignment": True}
        result = self.orchestrator.run_diagnostic_trace(incident, telemetry)
        
        self.assertTrue(result["can_actuate"])
        self.assertEqual(result["trace_result"]["status"], "CLEARED")

    def test_triage_blocked_at_apparatus(self):
        """Test that triage stops if physical integrity is unverified."""
        incident = "Coffee maker brewing at midnight"
        telemetry = {"physical_integrity": False} # Loose connection
        
        result = self.orchestrator.run_diagnostic_trace(incident, telemetry)
        
        self.assertFalse(result["can_actuate"])
        self.assertEqual(result["trace_result"]["layer"], "APPARATUS")
        self.assertIn("Verify physical integrity", result["trace_result"]["message"])

    def test_triage_blocked_at_harness(self):
        """Test blocking at the harness layer (Operational Context)."""
        incident = "Thermostat reset to 85 degrees"
        telemetry = {"physical_integrity": True, "logical_consistency": True, "environmental_alignment": False}
        
        result = self.orchestrator.run_diagnostic_trace(incident, telemetry)
        
        self.assertFalse(result["can_actuate"])
        self.assertEqual(result["trace_result"]["layer"], "HARNESS")

if __name__ == "__main__":
    unittest.main()
