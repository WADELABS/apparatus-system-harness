# Hello World Demo

This is the simplest possible example of using the Apparatus System Harness. It demonstrates the core workflow in under 5 seconds without any external dependencies.

## What This Demo Does

1. **Creates a Manifest** - Defines an inquiry declaratively
2. **Parses the Manifest** - Converts YAML/dict to structured data
3. **Validates the Manifest** - Ensures correctness using Pydantic schemas
4. **Executes the Inquiry** - Runs the instruments defined in the manifest
5. **Displays Results** - Shows human-readable output

## Running the Demo

### Prerequisites

- Python 3.9+
- Virtual environment activated
- Dependencies installed (`pip install -e .`)

### Run It

```bash
# From the repository root
python examples/hello-world/demo.py
```

### Expected Output

```
============================================================
  🏛️  Apparatus System Harness - Hello World Demo
============================================================

This demo demonstrates the core manifest-driven workflow:
  • Declarative YAML manifests define all behavior
  • Zero configuration drift
  • Immutable audit trails
  • Reproducible deployments

Step 1: Creating manifest...
✓ Manifest created
   Manifest ID: hello_world_demo
   Instruments: 1
   Phases: 3

Step 2: Parsing manifest...
✓ Manifest parsed successfully

Step 3: Validating manifest...
✓ Manifest is valid

Step 4: Executing inquiry...
✓ Inquiry completed

Step 5: Results

Inquiry Results
------------------------------------------------------------

1. Phase: initialization
   Status: Success
   Echo: {'phase': 'initialization', 'message': 'Executing initialization phase', 'timestamp': '2026-02-16T...'}
   Timestamp: ...

2. Phase: execution
   Status: Success
   Echo: {'phase': 'execution', 'message': 'Executing execution phase', 'timestamp': '2026-02-16T...'}
   Timestamp: ...

3. Phase: analysis
   Status: Success
   Echo: {'phase': 'analysis', 'message': 'Executing analysis phase', 'timestamp': '2026-02-16T...'}
   Timestamp: ...

------------------------------------------------------------
✓ All phases completed successfully

============================================================
  Demo Completed Successfully! 🎉
============================================================

Next Steps:
  • Explore the manifest file: sample-manifest.yaml
  • Read the documentation: docs/local-quickstart.md
  • Try the advanced demo: python portfolio_demo.py
  • Learn about the seven layers: docs/layers.md
```

## What's Happening Under the Hood

### 1. Manifest Creation

The manifest defines everything about the inquiry:
- What instruments to use
- What phases to execute
- How to handle concurrency and retries
- What reports to generate

This is the **Manifest-Over-Code** philosophy in action.

### 2. Parsing

The `ManifestParser` reads the manifest and ensures it's well-formed. In production, this would read from YAML files tracked in Git.

### 3. Validation

The `ManifestValidator` uses Pydantic models to enforce:
- Type safety
- Required fields
- Value constraints
- Semantic correctness

This prevents invalid configurations from ever reaching production.

### 4. Execution

The demo creates an `EchoInstrument` (Layer 2 - Holonic Instruments) and executes it for each phase defined in the protocol.

In the full system, execution includes:
- **Layer 1**: Raft consensus for HA
- **Layer 2**: Modular instruments
- **Layer 3**: Hermeneutic synthesis (multi-source arbitration)
- **Layer 4**: Apophatic falsification (excludes invalid data)
- **Layer 5**: RBAC gating (authorization)
- **Layer 6**: Quantum state simulation (probabilistic tracking)
- **Layer 7**: Substrate sandboxing (isolated execution)

### 5. Results

Results are displayed to the console. In production, they would be:
- Written to a verified state ledger
- Stored as compliance artifacts
- Published to monitoring systems
- Cryptographically signed for audit trails

## Files in This Directory

- **demo.py** - Main demo script (well-commented for learning)
- **sample-manifest.yaml** - Example manifest file showing YAML format
- **README.md** - This file

## Customizing the Demo

### Modify the Manifest

Edit `sample-manifest.yaml` to change:
- Number of instruments
- Execution phases
- Protocol type (sequential, parallel, dag)
- Instrument parameters

### Change Instrument Type

Replace `EchoInstrument` with other instruments:

```python
# Try the SensitivityProbe
from inquisitor.instruments.behavioral.sensitivity_probe import SensitivityProbe

# Or the WeightAnalyzer
from inquisitor.instruments.structural.weight_analyzer import WeightAnalyzer
```

### Add Validation Logic

Extend the validation step to include custom checks:

```python
async def validate_manifest(parsed_manifest):
    # Standard validation
    validator = ManifestValidator()
    result = await validator.validate(parsed_manifest)
    
    # Custom validation
    if not custom_business_logic_check(parsed_manifest):
        print_error("Custom validation failed!")
        return None
    
    return parsed_manifest
```

## Key Concepts Demonstrated

1. **Declarative Configuration**: All behavior defined in manifest
2. **Validation-First**: Catch errors before execution
3. **Type Safety**: Pydantic models ensure correctness
4. **Async Execution**: Modern Python async/await patterns
5. **Separation of Concerns**: Parser, Validator, Executor are independent

## What This Demo Doesn't Show

This simplified demo focuses on the core workflow. It doesn't demonstrate:

- **Raft Consensus** (Layer 1) - Distributed leader election
- **gRPC Communication** (Layer 2) - Remote instrument protocols
- **Multi-Source Synthesis** (Layer 3) - Combining data from multiple sources
- **Falsification Logic** (Layer 4) - Excluding invalid data
- **RBAC Authorization** (Layer 5) - Multi-tenant access control
- **Quantum State** (Layer 6) - Probabilistic uncertainty tracking
- **Sandboxed Execution** (Layer 7) - Isolated untrusted probes

For these advanced features, see:
- `portfolio_demo.py` - Full 7-layer demonstration
- `docs/layers.md` - Deep dive into each layer
- `tests/integration/` - Integration test examples

## Troubleshooting

### Import Errors

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Install in development mode
pip install -e .
```

### Module Not Found

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Run from repository root
cd /path/to/apparatus-system-harness
python examples/hello-world/demo.py
```

### Validation Errors

If the manifest fails validation:
1. Check the error messages carefully
2. Compare against `sample-manifest.yaml`
3. Review `docs/manifest-schema.md` for schema details
4. Ensure all required fields are present

## Next Steps

1. **Read the Docs**: Start with `docs/local-quickstart.md`
2. **Try the Advanced Demo**: Run `python portfolio_demo.py`
3. **Explore Layers**: Read `docs/layers.md`
4. **Write Your Own Manifest**: Use `sample-manifest.yaml` as a template
5. **Check the Tests**: See `tests/unit/test_validator.py` for examples

## Questions?

- Check the [documentation](../../docs/)
- Review [existing issues](https://github.com/WADELABS/apparatus-system-harness/issues)
- Read the [architecture overview](../../docs/architecture.md)

Happy hacking! 🏛️
