"""
Unit tests for Synthesis Engine.
Tests HermeneuticSynthesizer and ApophaticVerifier.
"""

import pytest
from inquisitor.synthesis.arbitrator import HermeneuticSynthesizer, ApophaticVerifier


class TestHermeneuticSynthesizer:
    """Test suite for HermeneuticSynthesizer."""
    
    @pytest.fixture
    def synthesizer(self):
        """Create a HermeneuticSynthesizer instance."""
        return HermeneuticSynthesizer()
    
    def test_synthesizer_initialization(self, synthesizer):
        """Test synthesizer initialization."""
        assert synthesizer is not None
    
    def test_synthesize_single_source(self, synthesizer):
        """Test synthesis with single data source."""
        instrument_outputs = [
            {'raw_data': '100.5', 'confidence_score': 0.95, 'source': 'sensor_1'}
        ]
        
        result = synthesizer.synthesize_findings(instrument_outputs)
        
        assert result['status'] == 'VERIFIED'
        assert result['synthesized_value'] == 100.5
        assert result['confidence'] == 0.95
    
    def test_synthesize_multiple_sources(self, synthesizer):
        """Test synthesis with multiple data sources."""
        instrument_outputs = [
            {'raw_data': '100.0', 'confidence_score': 0.9, 'source': 'sensor_1'},
            {'raw_data': '102.0', 'confidence_score': 0.8, 'source': 'sensor_2'},
            {'raw_data': '101.0', 'confidence_score': 0.85, 'source': 'sensor_3'}
        ]
        
        result = synthesizer.synthesize_findings(instrument_outputs)
        
        assert result['status'] == 'VERIFIED'
        assert 'synthesized_value' in result
        # Should be weighted average
        assert 100.0 <= result['synthesized_value'] <= 102.0
        assert 'confidence' in result
    
    def test_synthesize_no_data(self, synthesizer):
        """Test synthesis with no data."""
        result = synthesizer.synthesize_findings([])
        
        assert result['status'] == 'INCONCLUSIVE'
        assert 'message' in result
    
    def test_synthesize_zero_confidence(self, synthesizer):
        """Test synthesis with zero confidence readings."""
        instrument_outputs = [
            {'raw_data': '100.0', 'confidence_score': 0.0, 'source': 'sensor_1'}
        ]
        
        result = synthesizer.synthesize_findings(instrument_outputs)
        
        assert result['status'] == 'INCONCLUSIVE'
    
    def test_synthesize_confidence_weighting(self, synthesizer):
        """Test that confidence weighting works correctly."""
        instrument_outputs = [
            {'raw_data': '100.0', 'confidence_score': 1.0, 'source': 'high_conf'},
            {'raw_data': '200.0', 'confidence_score': 0.1, 'source': 'low_conf'}
        ]
        
        result = synthesizer.synthesize_findings(instrument_outputs)
        
        # Should be weighted toward high confidence value
        assert result['synthesized_value'] < 150.0  # Closer to 100 than 200
    
    def test_synthesize_negative_value(self, synthesizer):
        """Test synthesis with negative values."""
        instrument_outputs = [
            {'raw_data': '-50.0', 'confidence_score': 0.9, 'source': 'sensor_1'}
        ]
        
        result = synthesizer.synthesize_findings(instrument_outputs)
        
        assert result['status'] == 'INVALID'
        assert result['synthesized_value'] < 0


class TestApophaticVerifier:
    """Test suite for ApophaticVerifier."""
    
    @pytest.fixture
    def verifier(self):
        """Create an ApophaticVerifier instance."""
        return ApophaticVerifier()
    
    def test_verifier_initialization(self, verifier):
        """Test verifier initialization."""
        assert verifier is not None
        assert len(verifier.exclusion_rules) > 0
    
    def test_verify_valid_value(self, verifier):
        """Test verification of valid value."""
        assert verifier.verify_possibility(100.5) is True
        assert verifier.verify_possibility(50.0) is True
        assert verifier.verify_possibility(999.0) is True
    
    def test_verify_negative_value(self, verifier):
        """Test verification rejects negative values."""
        assert verifier.verify_possibility(-10.0) is False
        assert verifier.verify_possibility(-0.001) is False
    
    def test_verify_unrealistic_spike(self, verifier):
        """Test verification rejects unrealistic spikes."""
        assert verifier.verify_possibility(2000000) is False
        assert verifier.verify_possibility(10000000) is False
    
    def test_verify_edge_cases(self, verifier):
        """Test verification at boundary values."""
        assert verifier.verify_possibility(0.0) is True
        assert verifier.verify_possibility(1000000) is True
        assert verifier.verify_possibility(1000001) is False
    
    def test_falsification_logic(self, verifier):
        """Test via negativa (falsification) logic."""
        # Apophatic logic: truth defined by what is excluded
        invalid_values = [-100, -1, 5000000, 10000000]
        valid_values = [0, 1, 100, 999999]
        
        for val in invalid_values:
            assert verifier.verify_possibility(val) is False
        
        for val in valid_values:
            assert verifier.verify_possibility(val) is True
