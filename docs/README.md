# Apparatus System Harness Documentation

Welcome to the Apparatus System Harness documentation! This directory contains comprehensive guides for understanding, using, and deploying the framework.

## Quick Links

### Getting Started
- **[Local Development Quick Start](local-quickstart.md)** - Set up and run the framework locally in minutes
- **[Hello World Example](../examples/hello-world/)** - Simple demo to understand the core workflow

### Core Concepts
- **[Architecture Overview](architecture.md)** - System design and manifest-over-code philosophy
- **[Seven Layers Deep Dive](layers.md)** - In-depth exploration of all 7 architectural layers
- **[Manifest Schema Reference](manifest-schema.md)** - Complete manifest specification with examples

### Deployment
- **[Kubernetes Deployment](deployment.md)** - Production deployment guide for Kubernetes
- **[Container Images](deployment.md#container-images)** - Using Docker containers

### Contributing
- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](../CHANGELOG.md)** - Project history and releases

## Documentation Structure

### [Architecture Overview](architecture.md)
Comprehensive overview of the system architecture, including:
- Manifest-Over-Code philosophy
- Core components (Parser, Validator, Compiler, Conductor)
- Data flow and execution pipeline
- Performance and resilience features

### [Seven Layers Deep Dive](layers.md)
Detailed documentation of the seven-layer architecture:
- **Core**: Manifest System (97% test coverage)
- **Layer 1**: HA Conductor (Raft Consensus)
- **Layer 2**: Holonic gRPC Instruments
- **Layer 3**: Hermeneutic Synthesis Engine
- **Layer 4**: Apophatic Falsification Engine
- **Layer 5**: Multi-Tenant Manifest Gating
- **Layer 6**: Quantum State Simulation
- **Layer 7**: Substrate Sandboxing

Each layer includes:
- Purpose and capabilities
- Current implementation status
- Code examples
- Key components

### [Manifest Schema Reference](manifest-schema.md)
Complete manifest schema documentation:
- Top-level structure
- Field definitions and types
- Validation rules
- Complete examples (minimal, multi-instrument, complex)
- Schema evolution and versioning
- Best practices

### [Local Development Guide](local-quickstart.md)
Step-by-step guide for local development:
- Installation instructions
- Running the Hello World demo
- Project structure overview
- Creating your first manifest
- Testing and debugging
- Troubleshooting common issues

### [Kubernetes Deployment Guide](deployment.md)
Production deployment instructions:
- Container images and tags
- Helm chart deployment
- Manual Kubernetes deployment
- Raft cluster configuration
- Monitoring and observability
- Security best practices
- Backup and disaster recovery
- Troubleshooting

## Additional Resources

### Example Code
- **[Hello World Demo](../examples/hello-world/)** - Simple introductory example
- **[Portfolio Demo](../portfolio_demo.py)** - Advanced 7-layer demonstration
- **[Sample Manifests](../manifests/)** - Example manifest files

### Schema Files
- **[JSON Schema](../schemas/inquiry-manifest-v1.schema.json)** - Machine-readable schema

### Development Tools
- **[Schema Generator](../scripts/generate-schema.py)** - Generate JSON Schema from Pydantic models

## Getting Help

- **Read the Docs**: Start with the [Local Quick Start](local-quickstart.md)
- **Try Examples**: Run `python examples/hello-world/demo.py`
- **Check Issues**: Browse [GitHub Issues](https://github.com/WADELABS/apparatus-system-harness/issues)
- **Join Discussions**: Participate in [GitHub Discussions](https://github.com/WADELABS/apparatus-system-harness/discussions)

## Contributing to Documentation

Documentation improvements are always welcome! When contributing documentation:

1. Keep explanations clear and concise
2. Include code examples where helpful
3. Update the table of contents when adding new sections
4. Test all commands and code snippets
5. Follow the existing documentation style

See the [Contributing Guide](../CONTRIBUTING.md) for more details.

---

*Last updated: 2026-02-16*
