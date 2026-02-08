"""
The Inquisitor Framework
========================

A manifest-driven, protocol-based framework for automated inquiry.

Core Components:
- core: The heart of the system (Manifests, Protocol Engine, Registry)
- instruments: The tools of inquiry (Probes, Gauges, Analyzers)
- substrates: The data sources (Datasets, Streams, Scrapers)
- analysis: The synthesis layer (Statistics, Topology, Visualization)
"""

__version__ = "0.1.0"

from .core.protocol_engine.conductor import AssayConductor
from .core.manifest_system.parser import ManifestParser
from .instruments.base.instrument import AbstractInstrument

__all__ = ["AssayConductor", "ManifestParser", "AbstractInstrument"]
