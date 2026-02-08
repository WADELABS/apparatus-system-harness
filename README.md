# The Inquisitor Framework
### An Epistemology of Automated Inquiry

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Helm](https://img.shields.io/badge/helm-v3-blue)

The **Inquisitor Framework** is a robust, declarative system for automated inquiry and data provenance. It rejects hard-coded logic in favor of **Manifest-Over-Code**, where the "truth" is defined by executable specifications.

> **Core Philosophy**: "We do not just get answers; we get the history of the question."

## 🚀 Key Features

*   **Declarative Manifests**: Define *what* to know, not *how* to find it.
*   **Holonic Architecture**: Composed of self-reliant, autonomous units (Instruments) that form a cohesive whole.
*   **Resilient Conductor**: Fault-tolerant orchestration of complex, multi-phase inquiry protocols.
*   **Immutable Registry**: Cryptographically verifiable history of all findings and execution traces.
*   **Kubernetes Native**: Fully containerized and deployable via Helm.

## 🛠️ Architecture

The system operates on a strict protocol:

1.  **Submission**: A `Manifest` defines the inquiry scope.
2.  **Orchestration**: The `Conductor` compiles an `ExecutionPlan`.
3.  **Observation**: `Instruments` probe `Substrates` (APIs, Filesystems, Networks).
4.  **Synthesis**: Data is harmonized into `Findings`.
5.  **Registry**: All outputs are hashed and stored.

## 📦 Getting Started

### Prerequisites
*   Python 3.9+
*   Docker & Kubernetes (for deployment)
*   Helm 3+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/apparatus-system-harness.git
cd apparatus-system-harness

# Install dependencies
pip install -e .
```

### Running Tests

Ensure the system is functioning correctly by running the integration suite:

```bash
python -m pytest tests/integration/test_full_assay.py
```

## ☸️ Deployment

 The framework is designed for Kubernetes. A production-ready Helm chart is included.

```bash
# Lint the chart
helm lint deployments/kubernetes/helm/inquisitor

# Deploy to cluster
helm install inquisitor ./deployments/kubernetes/helm/inquisitor -f deployments/kubernetes/helm/inquisitor/values.yaml
```

## 📄 Documentation

*   [Manifest Specification](MANIFEST.md)
*   [Helm Configuration](deployments/kubernetes/helm/inquisitor/values.yaml)

---
*Generated for the Apparatus System Harness v2.0*
