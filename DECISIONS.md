# Design Decisions: Apparatus System Harness

### Objective: Infrastructure as Code & Immutable Provenance

- **Decision 1: Manifest-Over-Code**: We prioritized declarative YAML manifests to eliminate procedural drift encountered in earlier scripting iterations.
- **Decision 2: Raft Consensus**: Selected for distributed state verification to ensure high availability during complex supply chain inquiries.
- **Decision 3: RBAC-Gated Access**: Enforced Multi-Tenant gating at Layer 5 to ensure that no single entity can compromise the verifiable timeline.
