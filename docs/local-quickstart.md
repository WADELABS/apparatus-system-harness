# Local Development Quick Start

This guide will help you set up and run the Apparatus System Harness locally without Kubernetes or Docker.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/WADELABS/apparatus-system-harness.git
cd apparatus-system-harness
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install the framework in development mode
pip install -e .

# Install development dependencies (optional)
pip install pytest pytest-asyncio pytest-cov black ruff
```

## Quick Start: Hello World Demo

The fastest way to get started is with our Hello World demo:

```bash
# Run the hello world demo
python examples/hello-world/demo.py
```

This demo:
- Defines a simple manifest
- Parses and validates it
- Executes a simple inquiry
- Displays results

Expected output:
```
🏛️ Apparatus System Harness - Hello World Demo
================================================

Step 1: Creating manifest...
✓ Manifest created

Step 2: Parsing manifest...
✓ Manifest parsed successfully

Step 3: Validating manifest...
✓ Manifest is valid

Step 4: Executing inquiry...
✓ Inquiry completed

Step 5: Results
----------------
[Results displayed here]
```

## Running the Advanced Demo

For a complete 7-layer demonstration:

```bash
python portfolio_demo.py
```

This demonstrates all layers working together including:
- Raft consensus
- Multi-instrument execution
- Hermeneutic synthesis
- Apophatic falsification
- RBAC gating
- Quantum state simulation
- Substrate sandboxing

## Project Structure

```
apparatus-system-harness/
├── src/inquisitor/              # Main package
│   ├── core/                    # Core manifest system
│   │   ├── manifest_system/     # Parser, validator, compiler
│   │   ├── protocol_engine/     # Orchestration
│   │   └── artifact_registry/   # Results storage
│   ├── conductor/               # Raft consensus
│   ├── instruments/             # Probe implementations
│   ├── synthesis/               # Hermeneutic & apophatic engines
│   ├── gated_access/            # RBAC & quantum simulation
│   └── registry/                # Sandboxing
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── examples/                    # Example code
│   └── hello-world/            # Simple getting started example
├── manifests/                   # Sample manifests
├── docs/                        # Documentation
└── portfolio_demo.py            # Full demo script
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=inquisitor --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run specific test file
pytest tests/unit/test_validator.py -v
```

## Code Formatting and Linting

```bash
# Format code with Black
black src/ tests/

# Lint code with Ruff
ruff check src/ tests/

# Type checking (if mypy is installed)
mypy src/
```

## Creating Your First Manifest

Create a file `my-inquiry.yaml`:

```yaml
manifest:
  version: "1.0.0"
  id: "my_first_inquiry"
  name: "My First Inquiry"
  
  metadata:
    author: "Your Name"
    description: "My first inquiry manifest"
    tags: ["learning", "demo"]
  
  protocol:
    type: "sequential"
    phases:
      - "execution"
  
  substrate:
    source:
      type: "synthetic"
      generator: "echo"
      parameters:
        prefix: "test_"
  
  instruments:
    - type: "echo"
      id: "echo_1"
      provider: "internal"
      parameters:
        mode: "echo"
```

### Validate Your Manifest

```python
import asyncio
from inquisitor.core.manifest_system import ManifestParser, ManifestValidator

async def validate_manifest():
    # Parse manifest
    parser = ManifestParser()
    manifest = await parser.parse("my-inquiry.yaml")
    
    # Validate
    validator = ManifestValidator()
    result = await validator.validate(manifest)
    
    if result.is_valid:
        print("✓ Manifest is valid!")
    else:
        print("✗ Validation errors:")
        for error in result.errors:
            print(f"  - {error}")

asyncio.run(validate_manifest())
```

## Working with Instruments

### Built-in Instruments

The framework includes several reference instruments:

1. **EchoInstrument** (`basic/echo_instrument.py`)
   - Simple echo functionality
   - Good for testing and learning

2. **SensitivityProbe** (`behavioral/sensitivity_probe.py`)
   - Behavioral analysis
   - Demonstrates parameter sensitivity

3. **WeightAnalyzer** (`structural/weight_analyzer.py`)
   - Structural analysis
   - Shows complex instrument patterns

### Using an Instrument

```python
from inquisitor.instruments.basic.echo_instrument import EchoInstrument

# Create instrument
instrument = EchoInstrument(
    instrument_id="echo_1",
    config={"mode": "echo"}
)

# Execute
result = await instrument.execute({"input": "Hello World"})
print(result)
```

## Using the Synthesis Engine

```python
from inquisitor.synthesis.arbitrator import HermeneuticSynthesizer

# Create synthesizer
synthesizer = HermeneuticSynthesizer()

# Arbitrate between readings
readings = [
    {"value": 22.5, "confidence": 0.9},
    {"value": 22.7, "confidence": 0.85},
    {"value": 22.4, "confidence": 0.95}
]

ground_truth = synthesizer.arbitrate(readings)
print(f"Ground truth: {ground_truth}")
```

## Troubleshooting

### Import Errors

If you get import errors:

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall in development mode
pip install -e .
```

### Module Not Found

If Python can't find the `inquisitor` module:

```bash
# Check your Python path
python -c "import sys; print('\n'.join(sys.path))"

# The src/ directory should be in the path
# If not, install with: pip install -e .
```

### Test Failures

If tests fail:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Try running a single test to isolate the issue
pytest tests/unit/test_validator.py::test_valid_manifest -v
```

### Permission Errors

If you get permission errors on Linux/Mac:

```bash
# Make sure scripts are executable
chmod +x examples/hello-world/demo.py

# Or run with python explicitly
python examples/hello-world/demo.py
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/my-feature
```

### 2. Make Changes

Edit code, add tests, update documentation.

### 3. Run Tests

```bash
pytest tests/ -v
```

### 4. Format and Lint

```bash
black src/ tests/
ruff check src/ tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "Add my feature"
```

### 6. Push and Create PR

```bash
git push origin feature/my-feature
# Then create a Pull Request on GitHub
```

## Environment Variables

The framework supports configuration via environment variables:

```bash
# Set log level
export LOG_LEVEL=DEBUG

# Set artifact output directory
export ARTIFACT_DIR=/path/to/artifacts

# Set manifest directory
export MANIFEST_DIR=/path/to/manifests
```

You can also create a `.env` file (see `.env.example`):

```bash
cp .env.example .env
# Edit .env with your settings
```

## Next Steps

- Read the [Architecture Overview](architecture.md) to understand the system design
- Explore the [Seven Layers](layers.md) in depth
- Study the [Manifest Schema Reference](manifest-schema.md)
- Check out more examples in `examples/`
- Read the [Contributing Guide](../CONTRIBUTING.md)

## Getting Help

- **Issues**: Check existing [GitHub issues](https://github.com/WADELABS/apparatus-system-harness/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/WADELABS/apparatus-system-harness/discussions)
- **Documentation**: Browse the [docs/](.) directory
- **Examples**: Study working examples in `examples/`

## Additional Resources

- [Architecture Overview](architecture.md)
- [Seven Layers Deep Dive](layers.md)
- [Manifest Schema Reference](manifest-schema.md)
- [Kubernetes Deployment](deployment.md)
- [Contributing Guide](../CONTRIBUTING.md)
