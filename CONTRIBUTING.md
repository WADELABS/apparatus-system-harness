# Contributing to Apparatus System Harness

Thank you for your interest in contributing to the Apparatus System Harness! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Manifest-Over-Code Philosophy](#manifest-over-code-philosophy)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Fork and Clone**

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/apparatus-system-harness.git
cd apparatus-system-harness

# Add upstream remote
git remote add upstream https://github.com/WADELABS/apparatus-system-harness.git
```

2. **Create Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov black ruff mypy
```

4. **Verify Installation**

```bash
# Run tests
pytest tests/ -v

# Run hello world demo
python examples/hello-world/demo.py
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clear, focused commits
- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Run Tests and Linters

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=inquisitor --cov-report=html

# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking (optional but recommended)
mypy src/
```

### 4. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with a clear message
git commit -m "Add feature: brief description"
```

Use conventional commit messages when possible:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style Guidelines

- Follow **PEP 8** conventions
- Use **type hints** for function signatures
- Write **docstrings** for classes and public methods
- Keep functions **focused and under 50 lines** when possible
- Use **async/await** patterns for I/O-bound operations

### Example

```python
async def validate_manifest(
    manifest: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None
) -> ValidationResult:
    """
    Validate a parsed manifest against the schema.
    
    Args:
        manifest: Parsed manifest dictionary
        context: Optional validation context
        
    Returns:
        ValidationResult with validation status and any errors
    """
    # Implementation here
    pass
```

### Formatting

We use **Black** for code formatting:

```bash
black src/ tests/
```

### Linting

We use **Ruff** for linting:

```bash
ruff check src/ tests/
```

## Testing

### Test Structure

```
tests/
├── unit/              # Unit tests for individual modules
├── integration/       # End-to-end integration tests
└── fixtures/          # Shared test fixtures
```

### Writing Tests

- **Write unit tests** for new functionality
- **Maintain >80% code coverage** for new code
- Use **pytest fixtures** for common test setup
- **Mock external dependencies** (file I/O, network calls, Raft replication)
- **Integration tests** should be idempotent and self-contained

### Example Test

```python
import pytest
from inquisitor.core.manifest_system import ManifestValidator

@pytest.mark.asyncio
async def test_valid_manifest():
    """Test validation of a valid manifest."""
    validator = ManifestValidator()
    manifest = {
        'manifest': {
            'version': '1.0.0',
            'id': 'test_id',
            # ... other required fields
        }
    }
    
    result = await validator.validate(manifest)
    assert result.is_valid
    assert len(result.errors) == 0
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_validator.py -v

# Run specific test
pytest tests/unit/test_validator.py::test_valid_manifest -v

# Run with coverage
pytest tests/ --cov=inquisitor --cov-report=html

# Open coverage report
open htmlcov/index.html  # On Mac
xdg-open htmlcov/index.html  # On Linux
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def process_manifest(manifest: Dict[str, Any], options: Dict[str, Any]) -> Result:
    """
    Process a manifest with given options.
    
    This function parses and validates the manifest, then compiles it
    into an execution plan.
    
    Args:
        manifest: The manifest dictionary to process
        options: Processing options (e.g., strict mode, validation level)
        
    Returns:
        Result object containing the processed manifest and any metadata
        
    Raises:
        ValidationError: If the manifest fails validation
        CompilationError: If the execution plan cannot be generated
        
    Example:
        >>> manifest = load_manifest("example.yaml")
        >>> result = process_manifest(manifest, {"strict": True})
        >>> print(result.execution_plan)
    """
    pass
```

### Updating Documentation

When making changes, update relevant documentation:

- README.md - High-level changes only
- docs/ - Detailed documentation
- Docstrings - Function/class documentation
- Examples - Working code examples
- CHANGELOG.md - User-facing changes

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted (`black`)
- [ ] Code is linted (`ruff`)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (for user-facing changes)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code is formatted
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
```

### Review Process

1. **Automated Checks**: CI/CD will run tests and checks
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any requested changes
4. **Merge**: Once approved, your PR will be merged

## Manifest-Over-Code Philosophy

When contributing, remember the core principle: **all system behavior should be declaratively specified in YAML manifests**.

### Adding New Features

1. **Define the manifest schema first** - What YAML structure represents this feature?
2. **Update Pydantic validation models** - Add to `validator.py`
3. **Implement execution logic** - Add to `compiler.py` and relevant modules
4. **Add tests with sample manifests** - Create test manifests demonstrating the feature
5. **Document in README and docs/** - Update architecture overview if needed

### Example: Adding a New Instrument Type

```python
# 1. Define in manifest schema (validator.py)
class CustomInstrumentSpec(BaseModel):
    type: Literal['custom_type']
    parameters: CustomParams

# 2. Implement instrument (instruments/custom/)
class CustomInstrument(AbstractInstrument):
    async def execute(self, parameters, context):
        # Implementation
        pass

# 3. Add tests (tests/unit/test_custom_instrument.py)
async def test_custom_instrument():
    # Test with manifest
    pass

# 4. Add example manifest (manifests/custom-example.yaml)
manifest:
  version: "1.0.0"
  instruments:
    - type: "custom_type"
      # ...
```

## Getting Help

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Search existing [GitHub issues](https://github.com/WADELABS/apparatus-system-harness/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/WADELABS/apparatus-system-harness/discussions)
- **Examples**: Study working examples in `examples/` and `tests/`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Apparatus System Harness! 🏛️
