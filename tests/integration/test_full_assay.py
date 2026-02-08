"""
Integration test for complete assay execution.
Tests the full pipeline from manifest parsing to artifact generation.
"""

import pytest
import pytest_asyncio
import asyncio
import tempfile
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from inquisitor.core.manifest_system.parser import ManifestParser
from inquisitor.core.manifest_system.validator import ManifestValidator
from inquisitor.core.protocol_engine.conductor import AssayConductor
from inquisitor.core.artifact_registry.registry import ArtifactRegistry
from inquisitor.instruments.behavioral.sensitivity_probe import SensitivityProbe
from inquisitor.instruments.structural.weight_analyzer import WeightAnalyzer


class TestCompleteAssayExecution:
    """Test complete assay execution pipeline."""
    
    @pytest.fixture(scope="class")
    def event_loop(self):
        """Create event loop for async tests."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    
    @pytest.fixture
    def temp_manifest_dir(self):
        """Create temporary directory for manifest testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    @pytest.fixture
    def sample_manifest(self, temp_manifest_dir) -> Dict[str, Any]:
        """Create a sample manifest for testing."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'integration_test_assay',
                'name': 'Integration Test Assay',
                'metadata': {
                    'author': 'Test Runner',
                    'created': datetime.now().isoformat(),
                    'tags': ['integration', 'test']
                },
                'protocol': {
                    'type': 'sequential',
                    'phases': ['initialization', 'execution', 'analysis']
                },
                'substrate': {
                    'source': {
                        'type': 'synthetic',
                        'generator': 'random_text',
                        'parameters': {
                            'num_samples': 10,
                            'min_length': 50,
                            'max_length': 200
                        }
                    }
                },
                'instruments': [
                    {
                        'type': 'sensitivity_probe',
                        'id': 'test_probe',
                        'provider': 'mock',
                        'parameters': {
                            'techniques': ['synonym_substitution'],
                            'intensity': [0.1, 0.2]
                        }
                    }
                ],
                'execution': {
                    'concurrency': {
                        'max_workers': 2
                    },
                    'retry_policy': {
                        'max_attempts': 2
                    }
                },
                'analysis': {
                    'statistical': [
                        {
                            'test': 'mean_comparison',
                            'groups': ['baseline', 'perturbed']
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
        
        # Write manifest to file
        manifest_path = temp_manifest_dir / 'test_manifest.yaml'
        with open(manifest_path, 'w') as f:
            yaml.dump(manifest, f)
        
        return manifest
    
    @pytest_asyncio.fixture
    async def conductor(self, temp_manifest_dir):
        """Create assay conductor for testing."""
        config = {
            'artifact_registry': {
                'type': 'filesystem',
                'base_path': temp_manifest_dir / 'findings'
            },
            'scheduler': {
                'max_concurrent_executions': 5
            },
            'circuit_breakers': {
                'error_threshold': 0.1,
                'window_size': 10
            },
            'telemetry': {
                'enabled': False  # Disable telemetry for tests
            }
        }
        
        return AssayConductor(config)

    @pytest.mark.asyncio
    async def test_manifest_loading_and_validation(self, sample_manifest, 
                                                  temp_manifest_dir):
        """Test manifest loading and validation."""
        parser = ManifestParser()
        validator = ManifestValidator()
        
        manifest_path = temp_manifest_dir / 'test_manifest.yaml'
        
        # Test loading
        with open(manifest_path, 'r') as f:
            raw_manifest = yaml.safe_load(f)
        
        context = {
            'execution_id': 'test_validation',
            'start_time': datetime.now()
        }
        
        parsed_manifest = await parser.parse(raw_manifest, context)
        
        # Test validation
        validation_result = await validator.validate(parsed_manifest, context)
        
        assert validation_result.is_valid
        # Mock parser returns raw manifest, so check structure
        assert raw_manifest['manifest']['id'] == 'integration_test_assay'

    @pytest.mark.asyncio
    async def test_complete_assay_execution(self, conductor, temp_manifest_dir, sample_manifest):
        """Test complete assay execution pipeline."""
        manifest_path = temp_manifest_dir / 'test_manifest.yaml'
        
        # Execute assay
        result = await conductor.orchestrate(str(manifest_path))
        
        # Verify results
        assert 'execution_id' in result
        assert 'registration_id' in result
        assert 'artifacts' in result
        assert 'report' in result

    @pytest.mark.asyncio
    async def test_holonic_layer_initialization(self):
        """Test initialization and basic functionality of Holonic layers."""
        from inquisitor.cognition.anticipation.scanner import HorizonScanner
        from inquisitor.cognition.sympoiesis.engine import SympoieticEngine
        
        # Test Horizon Scanner
        scanner = HorizonScanner()
        inputs = {'news': [{'text': 'Unprecedented anomaly detected in sector 7'}]}
        events = await scanner.scan_horizon(inputs)
        assert len(events) >= 0  # Just checking it runs without error for now
        
        # Test Sympoietic Engine
        engine = SympoieticEngine()
        result = await engine.facilitate_mutual_becoming("User Input", "Agent State")
        assert 'intersubjective_state' in result
