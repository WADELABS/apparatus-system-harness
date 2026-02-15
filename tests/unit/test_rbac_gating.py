"""
Unit tests for RBAC Gating and Quantum State Simulation.
Tests InquiryGating authorization and QuantumStateSimulation.
"""

import pytest
from inquisitor.gated_access.rbac import InquiryGating, QuantumStateSimulation


class TestInquiryGating:
    """Test suite for InquiryGating (RBAC)."""
    
    @pytest.fixture
    def gating(self):
        """Create an InquiryGating instance."""
        return InquiryGating()
    
    def test_gating_initialization(self, gating):
        """Test gating initialization with default policies."""
        assert gating is not None
        assert 'risk_auditor' in gating.policies
        assert 'quant_alpha_desk' in gating.policies
        assert 'exchange_conn' in gating.policies
    
    def test_authorize_valid_access(self, gating):
        """Test authorization for valid tenant/manifest combination."""
        assert gating.authorize('risk_auditor', 'REGULATORY_CHECK') is True
        assert gating.authorize('quant_alpha_desk', 'PRICING_ARBITRAGE') is True
        assert gating.authorize('exchange_conn', 'FEED_STATUS') is True
    
    def test_authorize_invalid_access(self, gating):
        """Test authorization denial for invalid combinations."""
        assert gating.authorize('risk_auditor', 'PRICING_ARBITRAGE') is False
        assert gating.authorize('quant_alpha_desk', 'REGULATORY_CHECK') is False
        assert gating.authorize('exchange_conn', 'PRICING_ARBITRAGE') is False
    
    def test_authorize_nonexistent_tenant(self, gating):
        """Test authorization for non-existent tenant."""
        assert gating.authorize('nonexistent_tenant', 'SOME_MANIFEST') is False
    
    def test_authorize_nonexistent_manifest_type(self, gating):
        """Test authorization for non-existent manifest type."""
        assert gating.authorize('risk_auditor', 'NONEXISTENT_TYPE') is False
    
    def test_policy_enforcement(self, gating):
        """Test that policies are properly enforced."""
        # risk_auditor should have specific manifest types
        assert 'REGULATORY_CHECK' in gating.policies['risk_auditor']
        assert 'LATENCY_AUDIT' in gating.policies['risk_auditor']
        assert 'PRICING_ARBITRAGE' not in gating.policies['risk_auditor']
    
    def test_tenant_isolation(self, gating):
        """Test tenant isolation - each tenant has separate policies."""
        # Add custom tenant
        gating.policies['custom_tenant'] = {'CUSTOM_MANIFEST'}
        
        assert gating.authorize('custom_tenant', 'CUSTOM_MANIFEST') is True
        assert gating.authorize('risk_auditor', 'CUSTOM_MANIFEST') is False
    
    def test_multiple_manifest_types(self, gating):
        """Test tenant with multiple manifest types."""
        manifest_types = gating.policies['quant_alpha_desk']
        assert 'PRICING_ARBITRAGE' in manifest_types
        assert 'MARKET_DEPTH_PROBE' in manifest_types
        
        for manifest_type in manifest_types:
            assert gating.authorize('quant_alpha_desk', manifest_type) is True
    
    def test_dynamic_policy_update(self, gating):
        """Test dynamic policy updates."""
        # Add new manifest type to existing tenant
        gating.policies['risk_auditor'].add('NEW_AUDIT_TYPE')
        
        assert gating.authorize('risk_auditor', 'NEW_AUDIT_TYPE') is True


class TestQuantumStateSimulation:
    """Test suite for QuantumStateSimulation."""
    
    @pytest.fixture
    def qsim(self):
        """Create a QuantumStateSimulation instance."""
        return QuantumStateSimulation()
    
    def test_qsim_initialization(self, qsim):
        """Test quantum state simulation initialization."""
        assert qsim is not None
    
    def test_collapse_state_single_option(self, qsim):
        """Test state collapse with single option."""
        probabilities = {'STATE_A': 1.0}
        result = qsim.collapse_state(probabilities)
        
        assert result == 'STATE_A'
    
    def test_collapse_state_multiple_options(self, qsim):
        """Test state collapse with multiple options."""
        probabilities = {
            'HIGH_CONFIDENCE': 0.9,
            'LOW_CONFIDENCE': 0.1
        }
        result = qsim.collapse_state(probabilities)
        
        assert result == 'HIGH_CONFIDENCE'  # Should select highest probability
    
    def test_collapse_state_equal_probabilities(self, qsim):
        """Test state collapse with equal probabilities."""
        probabilities = {
            'STATE_A': 0.5,
            'STATE_B': 0.5
        }
        result = qsim.collapse_state(probabilities)
        
        # Should select one of them (max picks first in case of tie)
        assert result in ['STATE_A', 'STATE_B']
    
    def test_collapse_state_empty(self, qsim):
        """Test state collapse with no probabilities."""
        result = qsim.collapse_state({})
        
        assert result == 'UNKNOWN'
    
    def test_collapse_state_confidence_threshold(self, qsim):
        """Test state collapse respects confidence thresholds."""
        probabilities = {
            'VERIFIED': 0.95,
            'UNCERTAIN': 0.03,
            'INVALID': 0.02
        }
        result = qsim.collapse_state(probabilities)
        
        assert result == 'VERIFIED'
    
    def test_state_superposition(self, qsim):
        """Test probabilistic state tracking (superposition)."""
        # Multiple states with different probabilities
        probabilities = {
            'SENSOR_ACTIVE': 0.7,
            'SENSOR_INTERMITTENT': 0.2,
            'SENSOR_OFFLINE': 0.1
        }
        result = qsim.collapse_state(probabilities)
        
        assert result == 'SENSOR_ACTIVE'  # Highest probability
    
    def test_false_positive_reduction(self, qsim):
        """Test that quantum simulation reduces false positives."""
        # Scenario: intermittent sensor readings
        probabilities = {
            'COMPLIANT': 0.6,
            'VIOLATION_DETECTED': 0.4
        }
        result = qsim.collapse_state(probabilities)
        
        # Should collapse to most likely state
        assert result == 'COMPLIANT'
    
    def test_market_stability_scenario(self, qsim):
        """Test market stability verification scenario."""
        probabilities = {
            'MARKET_STABLE_VERIFIED': 0.96,
            'LIQUIDITY_ANOMALY_DETECTED': 0.04
        }
        result = qsim.collapse_state(probabilities)
        
        assert result == 'MARKET_STABLE_VERIFIED'
