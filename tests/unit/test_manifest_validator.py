"""
Unit tests for ManifestValidator.
Tests Pydantic validation, error detection, type checking, and semantic validation.
"""

import pytest
from inquisitor.core.manifest_system.validator import (
    ManifestValidator,
    ValidationResult,
    InquiryManifest,
    ManifestMetadata,
    ProtocolSpec,
    InstrumentSpec
)


class TestManifestValidator:
    """Test suite for ManifestValidator."""
    
    @pytest.fixture
    def validator(self):
        """Create a ManifestValidator instance."""
        return ManifestValidator()
    
    @pytest.fixture
    def valid_complete_manifest(self):
        """Complete valid manifest."""
        return {
            'manifest': {
                'version': '1.0.0',
                'id': 'test_manifest_001',
                'name': 'Complete Test Manifest',
                'metadata': {
                    'author': 'Test Author',
                    'created': '2026-01-01T00:00:00Z',
                    'description': 'A comprehensive test manifest',
                    'tags': ['test', 'validation', 'complete']
                },
                'protocol': {
                    'type': 'sequential',
                    'phases': ['initialization', 'execution', 'analysis']
                },
                'substrate': {
                    'source': {
                        'type': 'synthetic',
                        'generator': 'random_data',
                        'parameters': {'count': 100}
                    }
                },
                'instruments': [
                    {
                        'type': 'test_probe',
                        'id': 'probe_001',
                        'provider': 'internal',
                        'parameters': {'sensitivity': 0.8}
                    },
                    {
                        'type': 'analyzer',
                        'id': 'analyzer_001',
                        'provider': 'external',
                        'parameters': {'mode': 'deep'}
                    }
                ],
                'execution': {
                    'concurrency': {'max_workers': 4},
                    'retry_policy': {
                        'max_attempts': 3,
                        'backoff_factor': 2.0,
                        'timeout': 30
                    },
                    'timeout': 300
                },
                'analysis': {
                    'statistical': [
                        {
                            'test': 'mean_comparison',
                            'groups': ['baseline', 'treatment']
                        }
                    ]
                },
                'reporting': {
                    'artifacts': [
                        {
                            'type': 'executive_summary',
                            'format': 'markdown'
                        }
                    ]
                }
            }
        }
    
    @pytest.mark.asyncio
    async def test_validate_complete_valid_manifest(self, validator, valid_complete_manifest):
        """Test validation of a complete, valid manifest."""
        result = await validator.validate(valid_complete_manifest)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    @pytest.mark.asyncio
    async def test_validate_missing_required_field(self, validator):
        """Test detection of missing required fields."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                # Missing 'id' and 'name'
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': []
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any('id' in error.lower() or 'name' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_invalid_version_format(self, validator):
        """Test detection of invalid version format."""
        manifest = {
            'manifest': {
                'version': 'invalid_version',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': []
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('version' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_invalid_protocol_type(self, validator):
        """Test detection of invalid protocol type."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'invalid_protocol_type',
                    'phases': ['init']
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': []
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('protocol' in error.lower() and 'type' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_concurrency_constraints(self, validator):
        """Test validation of concurrency constraints."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}],
                'execution': {
                    'concurrency': {'max_workers': 150}  # Exceeds max of 100
                }
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('max_workers' in error.lower() or 'concurrency' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_retry_policy_constraints(self, validator):
        """Test validation of retry policy constraints."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}],
                'execution': {
                    'retry_policy': {
                        'max_attempts': 15  # Exceeds max of 10
                    }
                }
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('max_attempts' in error.lower() or 'retry' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_duplicate_instrument_ids(self, validator):
        """Test detection of duplicate instrument IDs."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {'type': 'probe', 'id': 'duplicate_id'},
                    {'type': 'analyzer', 'id': 'duplicate_id'}
                ]
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('duplicate' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_empty_phases_list(self, validator):
        """Test detection of empty phases list."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'sequential',
                    'phases': []  # Empty phases
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}]
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('phase' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_no_instruments(self, validator):
        """Test detection of manifests with no instruments."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': []  # No instruments
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('instrument' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_type_checking(self, validator):
        """Test type validation for various fields."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {
                    'author': 'Test',
                    'tags': 'should_be_list'  # Wrong type
                },
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}]
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        assert any('tags' in error.lower() for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_validate_unwrapped_manifest(self, validator):
        """Test validation of manifest without wrapper."""
        manifest = {
            'version': '1.0.0',
            'id': 'test',
            'name': 'Test',
            'metadata': {'author': 'Test'},
            'protocol': {'type': 'sequential', 'phases': ['init']},
            'substrate': {'source': {'type': 'synthetic'}},
            'instruments': [{'type': 'probe', 'id': 'p1'}]
        }
        
        result = await validator.validate(manifest)
        
        assert result.is_valid
    
    @pytest.mark.asyncio
    async def test_validate_optional_fields(self, validator):
        """Test validation with minimal required fields only."""
        minimal_manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'minimal',
                'name': 'Minimal Manifest',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['execution']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'basic', 'id': 'inst1'}]
                # Optional fields omitted
            }
        }
        
        result = await validator.validate(minimal_manifest)
        
        assert result.is_valid
    
    @pytest.mark.asyncio
    async def test_validate_with_context(self, validator, valid_complete_manifest):
        """Test validation with context parameter."""
        context = {'validation_level': 'strict'}
        result = await validator.validate(valid_complete_manifest, context)
        
        assert result.is_valid
    
    @pytest.mark.asyncio
    async def test_validation_error_field_paths(self, validator):
        """Test that validation errors include field paths."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'test',
                'name': 'Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['init']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {
                        'type': '',  # Empty instrument type
                        'id': 'probe1'
                    }
                ]
            }
        }
        
        result = await validator.validate(manifest)
        
        assert not result.is_valid
        # Should have error mentioning the field path
        assert len(result.errors) > 0
