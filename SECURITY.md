# Security Policy

## Supported Versions

Use the latest version of this framework to ensure you have the most up-to-date security patches.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of this research framework seriously. If you have discovered a security vulnerability, please do not disclose it publicly.

### Research Context
This repository contains experimental code ("The Crucible", "Negative Space", etc.) designed for investigating AI internals. Some tools are intentionally invasive (e.g., weight manipulation, memory injection). **Intended behavior used maliciously does not constitute a vulnerability in the tool itself**, but we are interested in bypasses of our safety guardrails.

### Reporting Process
1.  Email your findings to `security@wadelabs.io` (or the repository maintainer).
2.  Include a Proof of Concept (PoC) or detailed steps to reproduce.
3.  We will acknowledge receipt within 48 hours.
4.  We will provide a timeline for a fix (if applicable).

## Security Best Practices for Users
*   **Isolation**: Run this code in sandboxed environments (Docker, venv).
*   **Secrets**: Never commit API keys or credentials. Use `.env` files.
*   **Review**: Audit source code before running on production systems.
