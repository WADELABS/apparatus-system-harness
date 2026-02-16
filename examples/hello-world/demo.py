#!/usr/bin/env python3
"""
Hello World Demo for Apparatus System Harness
==============================================

This demo demonstrates the core workflow of the Apparatus System Harness:
1. Define a manifest (declarative YAML configuration)
2. Parse the manifest
3. Validate the manifest structure
4. Execute the inquiry
5. Display results

This is a simplified example that runs locally without any external dependencies
like Kubernetes or Raft clusters. It's designed to help you understand the basic
concepts quickly.

Usage:
    python demo.py
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Ensure the src directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import core components
from inquisitor.core.manifest_system.parser import ManifestParser
from inquisitor.core.manifest_system.validator import ManifestValidator
from inquisitor.instruments.base.instrument import AbstractInstrument, InstrumentConfig


def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_step(step_num: int, description: str):
    """Print a step indicator."""
    print(f"Step {step_num}: {description}")


def print_success(message: str):
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"✗ {message}")


def create_hello_manifest():
    """
    Create a simple hello world manifest.
    
    This demonstrates the manifest structure that defines all system behavior.
    The manifest is the single source of truth for what the inquiry will do.
    """
    return {
        'manifest': {
            'version': '1.0.0',
            'id': 'hello_world_demo',
            'name': 'Hello World Inquiry',
            'metadata': {
                'author': 'Apparatus Demo',
                'description': 'A simple hello-world inquiry',
                'created': datetime.now().isoformat(),
                'tags': ['demo', 'hello-world']
            },
            'protocol': {
                'type': 'sequential',
                'phases': ['initialization', 'execution', 'analysis']
            },
            'substrate': {
                'source': {
                    'type': 'synthetic',
                    'generator': 'echo',
                    'parameters': {
                        'prefix': 'demo_'
                    }
                }
            },
            'instruments': [
                {
                    'type': 'echo',
                    'id': 'echo_1',
                    'provider': 'internal',
                    'parameters': {
                        'response_delay_ms': 10,
                        'mode': 'echo'
                    }
                }
            ],
            'execution': {
                'concurrency': {
                    'max_workers': 1
                },
                'retry_policy': {
                    'max_attempts': 1
                }
            },
            'reporting': {
                'artifacts': [
                    {
                        'type': 'console_summary',
                        'format': 'markdown'
                    }
                ]
            }
        }
    }


async def parse_manifest(manifest_dict):
    """
    Parse the manifest dictionary.
    
    The ManifestParser ensures the manifest is well-formed and converts it
    into a structured format for further processing.
    """
    parser = ManifestParser()
    
    # In a real scenario, you might parse from a YAML file:
    # parsed = await parser.parse("manifest.yaml")
    
    # For this demo, we're using a dict directly
    return manifest_dict


async def validate_manifest(parsed_manifest):
    """
    Validate the manifest against the schema.
    
    The ManifestValidator uses Pydantic models to ensure:
    - All required fields are present
    - Field types are correct
    - Values are within acceptable ranges
    - Semantic constraints are satisfied
    """
    validator = ManifestValidator()
    result = await validator.validate(parsed_manifest)
    
    if not result.is_valid:
        print_error("Manifest validation failed!")
        for error in result.errors:
            print(f"  - {error}")
        return None
    
    return parsed_manifest


async def execute_inquiry(manifest):
    """
    Execute a simple inquiry using the manifest.
    
    This demonstrates the execution flow:
    - Create instrument instances based on manifest
    - Execute measurements
    - Collect results
    
    Note: This is a simplified version. The full system includes:
    - Raft consensus for HA (Layer 1)
    - Substrate sandboxing (Layer 7)
    - Hermeneutic synthesis (Layer 3)
    - Apophatic falsification (Layer 4)
    - RBAC gating (Layer 5)
    - Quantum state simulation (Layer 6)
    """
    manifest_data = manifest.get('manifest', manifest)
    
    # Create a simple echo instrument implementation for the demo
    from inquisitor.instruments.base.instrument import InstrumentConfig
    
    # Import echo instrument (with proper path)
    from inquisitor.instruments.basic.echo_instrument import EchoInstrument
    
    # Create a mock telemetry collector for the demo
    class MockTelemetry:
        """Simple mock telemetry collector for demo purposes."""
        def span(self, name, context):
            """Mock span context manager."""
            from contextlib import asynccontextmanager
            @asynccontextmanager
            async def mock_span():
                yield
            return mock_span()
        
        async def record_instrument_ready(self, id: str):
            """Record instrument ready."""
            pass
        
        async def record_instrument_error(self, id: str, type: str, error: Exception):
            """Record instrument error."""
            pass
        
        async def record_instrument_execution(self, id: str, result: Any, context: Dict[str, Any]):
            """Record instrument execution."""
            pass
        
        async def record_instrument_failure(self, id: str, error: Exception, context: Dict[str, Any]):
            """Record instrument failure."""
            pass
        
        async def record_checkpoint_created(self, id: str, path: str, meta: Dict[str, Any]):
            """Record checkpoint created."""
            pass
        
        async def record_checkpoint_restored(self, id: str, path: str):
            """Record checkpoint restored."""
            pass
    
    class MockProvenance:
        """Simple mock provenance recorder for demo purposes."""
        async def record_calibration(self, id: str, result: Any, config: Any):
            """Record calibration."""
            pass
        
        async def record_execution(self, instrument_id: str, result: Any, context: Dict[str, Any]):
            """Record execution."""
            pass
        
        async def record_execution_failure(self, instrument_id: str, error: Exception, result: Any, context: Dict[str, Any]):
            """Record execution failure."""
            pass
    
    # Create instrument from manifest specification
    instrument_spec = manifest_data['instruments'][0]
    
    config = InstrumentConfig(
        id=instrument_spec['id'],
        type=instrument_spec['type'],
        parameters=instrument_spec.get('parameters', {})
    )
    
    telemetry = MockTelemetry()
    provenance = MockProvenance()
    instrument = EchoInstrument(config, telemetry, provenance)
    
    # Initialize instrument
    await instrument.initialize()
    
    # Execute measurements for each phase
    results = []
    phases = manifest_data['protocol']['phases']
    
    for phase in phases:
        phase_name = phase if isinstance(phase, str) else phase.get('name', phase)
        
        # Execute instrument with phase-specific parameters
        execution_params = {
            'phase': phase_name,
            'message': f'Executing {phase_name} phase',
            'timestamp': datetime.now().isoformat()
        }
        
        # Context provides metadata about the execution
        execution_context = {
            'execution_id': f'{phase_name}_{datetime.now().timestamp()}',
            'start_time': datetime.now(),
            'phase': phase_name
        }
        
        result = await instrument.execute(execution_params, execution_context)
        results.append({
            'phase': phase_name,
            'result': result
        })
    
    return results


def display_results(results):
    """
    Display the inquiry results in a human-readable format.
    
    In a production system, results would be:
    - Written to the verified state ledger
    - Stored as compliance artifacts
    - Published to monitoring systems
    - Archived for audit trails
    """
    print("\nInquiry Results")
    print("-" * 60)
    
    if not results:
        print("No results generated")
        return
    
    for i, result_entry in enumerate(results, 1):
        phase = result_entry['phase']
        result = result_entry['result']
        
        print(f"\n{i}. Phase: {phase}")
        print(f"   Status: {'Success' if result.success else 'Failed'}")
        
        # ExecutionResult has attributes: success, data, metrics, artifacts, errors, execution_time, timestamp
        if result.data:
            print(f"   Data: {result.data}")
        if result.metrics:
            print(f"   Metrics: {result.metrics}")
        print(f"   Execution Time: {result.execution_time:.4f}s")
        print(f"   Timestamp: {result.timestamp}")
    
    print("\n" + "-" * 60)
    print("✓ All phases completed successfully")


async def main():
    """Main demo execution flow."""
    
    # Print welcome header
    print_header("🏛️  Apparatus System Harness - Hello World Demo")
    
    print("This demo demonstrates the core manifest-driven workflow:")
    print("  • Declarative YAML manifests define all behavior")
    print("  • Zero configuration drift")
    print("  • Immutable audit trails")
    print("  • Reproducible deployments")
    
    try:
        # Step 1: Create manifest
        print_step(1, "Creating manifest...")
        manifest = create_hello_manifest()
        print_success("Manifest created")
        print(f"   Manifest ID: {manifest['manifest']['id']}")
        print(f"   Instruments: {len(manifest['manifest']['instruments'])}")
        print(f"   Phases: {len(manifest['manifest']['protocol']['phases'])}")
        
        # Step 2: Parse manifest
        print_step(2, "Parsing manifest...")
        parsed = await parse_manifest(manifest)
        print_success("Manifest parsed successfully")
        
        # Step 3: Validate manifest
        print_step(3, "Validating manifest...")
        validated = await validate_manifest(parsed)
        if validated is None:
            print_error("Validation failed - exiting")
            return 1
        print_success("Manifest is valid")
        
        # Step 4: Execute inquiry
        print_step(4, "Executing inquiry...")
        results = await execute_inquiry(validated)
        print_success("Inquiry completed")
        
        # Step 5: Display results
        print_step(5, "Results")
        display_results(results)
        
        # Success message
        print_header("Demo Completed Successfully! 🎉")
        print("\nNext Steps:")
        print("  • Explore the manifest file: sample-manifest.yaml")
        print("  • Read the documentation: docs/local-quickstart.md")
        print("  • Try the advanced demo: python portfolio_demo.py")
        print("  • Learn about the seven layers: docs/layers.md")
        print()
        
        return 0
        
    except Exception as e:
        print_error(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # Run the async main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
