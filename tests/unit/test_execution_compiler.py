"""
Unit tests for ExecutionPlanCompiler.
Tests execution plan compilation, DAG construction, retry policies, and concurrency.
"""

import pytest
from inquisitor.core.manifest_system.compiler import (
    ExecutionPlanCompiler,
    ExecutionPlan,
    ExecutionStep
)
from inquisitor.core.manifest_system.parser import ManifestParser


class TestExecutionPlanCompiler:
    """Test suite for ExecutionPlanCompiler."""
    
    @pytest.fixture
    def compiler(self):
        """Create an ExecutionPlanCompiler instance."""
        return ExecutionPlanCompiler()
    
    @pytest.fixture
    def parser(self):
        """Create a ManifestParser instance."""
        return ManifestParser()
    
    @pytest.fixture
    def simple_sequential_manifest(self):
        """Simple sequential protocol manifest."""
        return {
            'manifest': {
                'version': '1.0.0',
                'id': 'sequential_test',
                'name': 'Sequential Test',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'sequential',
                    'phases': ['initialization', 'execution', 'analysis']
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {'type': 'probe_a', 'id': 'probe_1', 'parameters': {'key': 'val1'}},
                    {'type': 'probe_b', 'id': 'probe_2', 'parameters': {'key': 'val2'}}
                ],
                'execution': {
                    'concurrency': {'max_workers': 2},
                    'retry_policy': {'max_attempts': 3}
                }
            }
        }
    
    @pytest.fixture
    def parallel_manifest(self):
        """Parallel execution manifest."""
        return {
            'manifest': {
                'version': '1.0.0',
                'id': 'parallel_test',
                'name': 'Parallel Test',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'parallel',
                    'phases': ['execution']
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {'type': 'probe', 'id': f'probe_{i}'} for i in range(5)
                ],
                'execution': {
                    'concurrency': {'max_workers': 5}
                }
            }
        }
    
    @pytest.mark.asyncio
    async def test_compile_simple_sequential(self, compiler, simple_sequential_manifest):
        """Test compilation of simple sequential protocol."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert isinstance(result, ExecutionPlan)
        assert result.phases == ['initialization', 'execution', 'analysis']
        assert len(result.steps) > 0
        assert result.concurrency_limit == 2
        assert result.estimated_duration > 0
    
    @pytest.mark.asyncio
    async def test_compile_parallel_execution(self, compiler, parallel_manifest):
        """Test compilation with parallel execution."""
        result = await compiler.compile(parallel_manifest)
        
        assert isinstance(result, ExecutionPlan)
        assert len(result.steps) == 5
        assert result.concurrency_limit == 5
    
    @pytest.mark.asyncio
    async def test_compile_concurrency_limit(self, compiler, simple_sequential_manifest):
        """Test concurrency limit extraction."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert result.concurrency_limit == 2
    
    @pytest.mark.asyncio
    async def test_compile_retry_policy(self, compiler, simple_sequential_manifest):
        """Test retry policy compilation."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert result.retry_policy is not None
        assert result.retry_policy['max_attempts'] == 3
        assert 'backoff_factor' in result.retry_policy
    
    @pytest.mark.asyncio
    async def test_compile_execution_steps(self, compiler, simple_sequential_manifest):
        """Test execution step generation."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert len(result.steps) > 0
        for step in result.steps:
            assert isinstance(step, ExecutionStep)
            assert step.step_id
            assert step.phase in result.phases
            assert step.instrument_id
            assert step.instrument_type
    
    @pytest.mark.asyncio
    async def test_compile_with_detailed_phases(self, compiler):
        """Test compilation with detailed phase definitions."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'detailed_phases',
                'name': 'Detailed Phases Test',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'sequential',
                    'phases': [
                        {
                            'name': 'initialization',
                            'steps': [
                                {
                                    'name': 'setup',
                                    'type': 'diagnostic',
                                    'instrument': 'probe_1',
                                    'parameters': {'action': 'init'}
                                }
                            ]
                        },
                        {
                            'name': 'execution',
                            'steps': [
                                {
                                    'name': 'measure',
                                    'type': 'measurement',
                                    'instrument': 'probe_2',
                                    'parameters': {'mode': 'active'}
                                }
                            ]
                        }
                    ]
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {'type': 'basic', 'id': 'probe_1'},
                    {'type': 'advanced', 'id': 'probe_2'}
                ]
            }
        }
        
        result = await compiler.compile(manifest)
        
        assert len(result.steps) == 2
        assert result.steps[0].phase == 'initialization'
        assert result.steps[1].phase == 'execution'
    
    @pytest.mark.asyncio
    async def test_compile_estimated_duration(self, compiler, simple_sequential_manifest):
        """Test estimation of execution duration."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert result.estimated_duration > 0
        # With 2 instruments and 3 phases, should have reasonable estimate
        assert result.estimated_duration < 1000  # Reasonable upper bound
    
    @pytest.mark.asyncio
    async def test_compile_metadata(self, compiler, simple_sequential_manifest):
        """Test metadata extraction in execution plan."""
        result = await compiler.compile(simple_sequential_manifest)
        
        assert 'manifest_id' in result.metadata
        assert result.metadata['manifest_id'] == 'sequential_test'
        assert 'manifest_version' in result.metadata
        assert 'protocol_type' in result.metadata
        assert result.metadata['protocol_type'] == 'sequential'
        assert 'instrument_count' in result.metadata
    
    @pytest.mark.asyncio
    async def test_compile_empty_instruments(self, compiler):
        """Test compilation with no instruments."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'empty_test',
                'name': 'Empty Instruments',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['execution']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': []
            }
        }
        
        result = await compiler.compile(manifest)
        
        assert isinstance(result, ExecutionPlan)
        assert len(result.steps) == 0
        assert result.estimated_duration == 0
    
    @pytest.mark.asyncio
    async def test_compile_default_concurrency(self, compiler):
        """Test default concurrency when not specified."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'default_test',
                'name': 'Default Concurrency',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['execution']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}]
                # No execution config
            }
        }
        
        result = await compiler.compile(manifest)
        
        assert result.concurrency_limit == 1  # Default value
    
    @pytest.mark.asyncio
    async def test_compile_with_parsed_manifest(self, compiler, parser, simple_sequential_manifest):
        """Test compilation with ParsedManifest object."""
        parsed = await parser.parse(simple_sequential_manifest)
        result = await compiler.compile(parsed)
        
        assert isinstance(result, ExecutionPlan)
        assert len(result.phases) == 3
    
    @pytest.mark.asyncio
    async def test_compile_phase_distribution(self, compiler):
        """Test that instruments are distributed across phases."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'distribution_test',
                'name': 'Phase Distribution',
                'metadata': {'author': 'Test'},
                'protocol': {
                    'type': 'sequential',
                    'phases': ['initialization', 'execution', 'analysis']
                },
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [
                    {'type': f'probe_{i}', 'id': f'probe_{i}'} for i in range(6)
                ]
            }
        }
        
        result = await compiler.compile(manifest)
        
        # Check that steps are distributed across phases
        phases_used = set(step.phase for step in result.steps)
        assert len(phases_used) > 1  # Should use multiple phases
    
    @pytest.mark.asyncio
    async def test_compile_timeout_propagation(self, compiler):
        """Test that timeouts are propagated to steps."""
        manifest = {
            'manifest': {
                'version': '1.0.0',
                'id': 'timeout_test',
                'name': 'Timeout Test',
                'metadata': {'author': 'Test'},
                'protocol': {'type': 'sequential', 'phases': ['execution']},
                'substrate': {'source': {'type': 'synthetic'}},
                'instruments': [{'type': 'probe', 'id': 'p1'}],
                'execution': {
                    'timeout': 120,
                    'retry_policy': {'timeout': 30}
                }
            }
        }
        
        result = await compiler.compile(manifest)
        
        assert result.steps[0].timeout == 120
        assert result.steps[0].retry_policy['timeout'] == 30
    
    @pytest.mark.asyncio
    async def test_compile_with_context(self, compiler, simple_sequential_manifest):
        """Test compilation with context parameter."""
        context = {'optimization': 'speed'}
        result = await compiler.compile(simple_sequential_manifest, context)
        
        assert isinstance(result, ExecutionPlan)
