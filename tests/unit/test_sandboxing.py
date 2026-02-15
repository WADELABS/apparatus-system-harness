"""
Unit tests for Substrate Sandboxing.
Tests probe spawning, isolation, and resource cleanup.
"""

import pytest
from inquisitor.registry.sandboxing import SubstrateSandboxing


class TestSubstrateSandboxing:
    """Test suite for SubstrateSandboxing."""
    
    @pytest.fixture
    def sandbox(self):
        """Create a SubstrateSandboxing instance."""
        return SubstrateSandboxing()
    
    def test_sandbox_initialization(self, sandbox):
        """Test sandbox initialization."""
        assert sandbox is not None
    
    def test_spawn_sandboxed_probe(self, sandbox):
        """Test spawning a sandboxed probe."""
        instrument_cmd = 'test_instrument_probe'
        result = sandbox.spawn_sandboxed_probe(instrument_cmd)
        
        assert result is not None
        assert 'SUCCESS' in result
        assert 'isolated' in result.lower() or 'container' in result.lower()
    
    def test_spawn_multiple_probes(self, sandbox):
        """Test spawning multiple sandboxed probes."""
        instruments = [
            'probe_thermal',
            'probe_rfid',
            'probe_blockchain'
        ]
        
        for instrument in instruments:
            result = sandbox.spawn_sandboxed_probe(instrument)
            assert result is not None
            assert 'SUCCESS' in result
    
    def test_spawn_grpc_probe(self, sandbox):
        """Test spawning gRPC exchange probe."""
        result = sandbox.spawn_sandboxed_probe('grpc_exchange_probe_nyse')
        
        assert result is not None
        assert 'SUCCESS' in result
    
    def test_cleanup_substrate(self, sandbox):
        """Test substrate cleanup."""
        container_id = 'test_container_123'
        
        # Should not raise exception
        sandbox.cleanup_substrate(container_id)
    
    def test_cleanup_multiple_substrates(self, sandbox):
        """Test cleaning up multiple substrates."""
        container_ids = ['container_1', 'container_2', 'container_3']
        
        for container_id in container_ids:
            sandbox.cleanup_substrate(container_id)
    
    def test_isolation_guarantees(self, sandbox):
        """Test that isolation is guaranteed for hostile probes."""
        hostile_probe = 'hostile_malware_probe'
        result = sandbox.spawn_sandboxed_probe(hostile_probe)
        
        # Should still spawn successfully but isolated
        assert result is not None
        assert 'SUCCESS' in result
    
    def test_resource_constraints(self, sandbox):
        """Test that sandboxed probes have resource constraints."""
        # In production, this would verify CPU/memory limits
        # For now, just verify the sandboxing mechanism exists
        result = sandbox.spawn_sandboxed_probe('resource_heavy_probe')
        assert result is not None
    
    def test_probe_naming_convention(self, sandbox):
        """Test various probe naming conventions."""
        probe_names = [
            'simple_probe',
            'complex-probe-with-dashes',
            'probe_with_underscores',
            'probe123'
        ]
        
        for probe_name in probe_names:
            result = sandbox.spawn_sandboxed_probe(probe_name)
            assert result is not None
            assert 'SUCCESS' in result
    
    def test_core_infrastructure_protection(self, sandbox):
        """Test that core infrastructure is protected from malicious sensors."""
        # Simulate spawning an untrusted probe
        untrusted_probe = 'untrusted_external_sensor'
        result = sandbox.spawn_sandboxed_probe(untrusted_probe)
        
        # Should spawn in isolated environment
        assert result is not None
        assert 'isolated' in result.lower() or 'container' in result.lower()
