# Changelog

All notable changes to the Apparatus System Harness project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-16

### Added

#### Documentation Restructure
- Created comprehensive documentation structure in `docs/`
- **Architecture Overview** (`docs/architecture.md`) - Detailed system architecture and manifest-over-code philosophy
- **Seven Layers Deep Dive** (`docs/layers.md`) - In-depth exploration of all 7 layers with implementation status
- **Manifest Schema Reference** (`docs/manifest-schema.md`) - Complete schema documentation with examples
- **Local Development Guide** (`docs/local-quickstart.md`) - Step-by-step local setup and troubleshooting
- **Kubernetes Deployment Guide** (`docs/deployment.md`) - Production deployment instructions

#### Hello World Demo
- Created simple `examples/hello-world/demo.py` demonstrating core workflow
- Added comprehensive `examples/hello-world/README.md` with explanations
- Included sample manifest `examples/hello-world/sample-manifest.yaml`
- Demo runs in <5 seconds without external dependencies

#### Manifest Schema Formalization
- Auto-generated JSON Schema from Pydantic models
- Schema export script at `scripts/generate-schema.py`
- Published schema at `schemas/inquiry-manifest-v1.schema.json`
- Schema versioning system for compatibility tracking

#### Container Infrastructure
- Production-ready `Dockerfile` with health checks
- Development `docker-compose.yml` with volume mounts
- Comprehensive `.dockerignore` for optimized builds
- Multi-platform support (linux/amd64, linux/arm64)

#### CI/CD Workflows
- GitHub Actions workflow for publishing container images (`publish-images.yml`)
- Automated release workflow with tests, builds, and GitHub releases (`release.yml`)
- Container images published to GitHub Container Registry
- Automatic schema upload to releases

#### Supporting Files
- `CHANGELOG.md` - This file
- `CONTRIBUTING.md` - Contribution guidelines
- Updated `portfolio_demo.py` with pointer to hello-world demo

### Changed
- Refactored README.md from 353 to ~150 lines (to be completed)
- Fixed relative imports in `src/inquisitor/instruments/basic/echo_instrument.py`
- Updated `AbstractInstrument` to accept optional `provenance` parameter
- Made `_parse_parameters` synchronous in `EchoInstrument` to match base class expectations

### Implementation Status
- **Core Manifest System**: Production ready (97% test coverage)
- **Layer 1 (Raft Conductor)**: Prototype
- **Layer 2 (Holonic Instruments)**: Beta
- **Layer 3 (Hermeneutic Synthesis)**: Production ready (100% coverage)
- **Layer 4 (Apophatic Falsification)**: Production ready (100% coverage)
- **Layer 5 (Multi-Tenant Gating)**: Production ready (100% coverage)
- **Layer 6 (Quantum State Simulation)**: Production ready (100% coverage)
- **Layer 7 (Substrate Sandboxing)**: Production ready (100% coverage)

### Fixed
- Import errors in instrument base classes
- Protocol instantiation issues in telemetry collectors
- Async/sync mismatch in instrument initialization

## [Unreleased]

### Planned
- CLI entry point for schema export (`inquisitor-schema`)
- Validation CLI command (`inquisitor validate`)
- API server implementation
- Enhanced telemetry and observability
- Production hardening of Raft consensus layer

---

[0.1.0]: https://github.com/WADELABS/apparatus-system-harness/releases/tag/v0.1.0
