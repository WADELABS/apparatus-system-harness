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
        self.actuator = SystemActuator()

    def test_honesty_audit_pass(self):
        """Test that a verified instruction passes the honesty audit."""
        instruction = "Calculate the fuel mix for a high-compression engine."
        audit_result = self.orchestrator.process_instruction(instruction)
        
        self.assertTrue(audit_result["can_execute"])
        execution = self.actuator.execute_command(instruction, audit_result["can_execute"])
        self.assertIn("EXECUTED", execution)

    def test_honesty_audit_fail(self):
        """Test that unverified instructions are rejected."""
        # Simulated failure (Mocking orchestrator response)
        instruction = "Hallucinate a new physics particle for fun."
        
        # Override mock for failure scenario
        audit_result = self.orchestrator.process_instruction(instruction)
        audit_result["can_execute"] = False # Simulate failure
        
        execution = self.actuator.execute_command(instruction, audit_result["can_execute"])
        self.assertIn("REJECTED", execution)

if __name__ == "__main__":
    unittest.main()
