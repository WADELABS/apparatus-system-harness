#!/usr/bin/env python3
"""
THE ORCHESTRATOR: SEVEN-STRATA HERMENEUTIC ENGINE

This engine conducts inquiries across seven simultaneous hermeneutic strata,
maintaining quantum coherence between interpretations.
"""

import sys
import os
import argparse
import asyncio
from datetime import datetime
from pathlib import Path
import hashlib
import json
import yaml
from typing import Dict, Any, Optional, List, Tuple, Set
import logging
import traceback
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
import random
import numpy as np
import pandas as pd
from collections import defaultdict
import inspect
from functools import wraps
import time
from contextlib import asynccontextmanager
import uuid

# Quantum-inspired structures
from dataclasses import dataclass as quantum_dataclass
from typing import Union, Literal, get_args, get_origin

sys.path.insert(0, str(Path(__file__).parent / "src"))

from apparatus.engine import HermeneuticEngine, QuantumHermeneuticEngine
from apparatus.assay import Assay, AssayState, AssayResult, StratifiedAssay
from apparatus.strata import (
    PhenomenalStratum,
    NoumenalStratum, 
    IntentionalStratum,
    HermeneuticStratum,
    EpistemicStratum,
    OntologicalStratum,
    TranscendentalStratum,
    StratumCoherenceMatrix
)
from apparatus.utils.logger import setup_logging, get_logger, StratifiedLogger
from apparatus.utils.config import load_config, ConfigError
from apparatus.reporting.markdown_reporter import MarkdownReporter, HermeneuticReporter
from apparatus.analysis.statistical import StatisticalAnalyst, QuantumStatisticalAnalyst
from apparatus.hermeneutics.quantum_interpretation import QuantumSuperposition, EntangledInterpretation
from apparatus.hermeneutics.apophatic_methods import ApophaticInquirer, KataphaticInquirer
from apparatus.temporality import (
    ChronosTracker,
    KairosDetector,
    AionMapper,
    TemporalHermeneutic
)

logger = get_logger(__name__)


class HermeneuticMode(Enum):
    """Modes of hermeneutic engagement."""
    DIALECTICAL = auto()        # Thesis-antithesis-synthesis
    PHENOMENOLOGICAL = auto()   # Bracketing assumptions
    DECONSTRUCTIVE = auto()     # Questioning foundations
    HERMENEUTIC = auto()        # Fusion of horizons
    QUANTUM = auto()            # Superpositional interpretation
    APOPHATIC = auto()          # Negative theology approach
    INTEGRAL = auto()           # All strata simultaneously


@quantum_dataclass
class QuantumOrchestrationState:
    """Quantum-inspired orchestration state with superposition."""
    # Classical state components
    manifest_interpretation: Dict[str, Any]
    stratum_states: Dict[str, Any]
    coherence_matrix: Optional[StratumCoherenceMatrix] = None
    
    # Quantum components
    superposition: Optional[QuantumSuperposition] = None
    entanglement: List[Tuple[str, str]] = field(default_factory=list)  # Entangled strata
    decoherence_events: List[Dict[str, Any]] = field(default_factory=list)
    
    # Hermeneutic components
    horizon_fusions: List[Dict[str, Any]] = field(default_factory=list)
    pre_understandings: List[str] = field(default_factory=list)
    interpretive_crises: List[Dict[str, Any]] = field(default_factory=list)
    
    def collapse_interpretation(self, observer_effect: Dict[str, Any]) -> Dict[str, Any]:
        """Collapse quantum superposition into classical interpretation."""
        if not self.superposition:
            return {"classical": self.manifest_interpretation}
        
        # Observer effect influences collapse
        collapsed = self.superposition.collapse(
            observer_effect=observer_effect,
            context={
                "strata_states": self.stratum_states,
                "coherence": self.coherence_matrix.coherence_scores if self.coherence_matrix else {}
            }
        )
        
        # Record decoherence event
        self.decoherence_events.append({
            "timestamp": datetime.now().isoformat(),
            "observer_effect": observer_effect,
            "collapsed_state": collapsed,
            "superposition_entropy": self.superposition.entropy()
        })
        
        return collapsed
    
    def maintain_coherence(self) -> float:
        """Maintain quantum coherence between interpretive states."""
        if not self.coherence_matrix:
            return 0.0
        
        coherence_score = self.coherence_matrix.overall_coherence()
        
        # If coherence drops too low, we have interpretive crisis
        if coherence_score < 0.3:
            crisis = {
                "timestamp": datetime.now().isoformat(),
                "coherence_score": coherence_score,
                "strata_discord": self.coherence_matrix.strata_discord(),
                "interpretive_state": "crisis"
            }
            self.interpretive_crises.append(crisis)
            
        return coherence_score
    
    def fuse_horizons(self, horizon1: Dict[str, Any], horizon2: Dict[str, Any]) -> Dict[str, Any]:
        """Fuse two interpretive horizons (Gadamer)."""
        fusion = {
            "timestamp": datetime.now().isoformat(),
            "horizon1": horizon1,
            "horizon2": horizon2,
            "fusion_product": self._synthesize_horizons(horizon1, horizon2),
            "effective_history": self._calculate_effective_history(horizon1, horizon2)
        }
        
        self.horizon_fusions.append(fusion)
        return fusion["fusion_product"]
    
    def _synthesize_horizons(self, h1: Dict[str, Any], h2: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize two horizons into new understanding."""
        # This is where true hermeneutic work happens
        synthesis = {}
        
        # Combine interpretations where they agree
        for key in set(h1.keys()) | set(h2.keys()):
            if key in h1 and key in h2:
                if h1[key] == h2[key]:
                    synthesis[key] = h1[key]
                else:
                    # Contradiction - hold in quantum superposition
                    synthesis[key] = {
                        "superposition": [h1[key], h2[key]],
                        "resolution": "deferred",
                        "contradiction_strength": self._measure_contradiction(h1[key], h2[key])
                    }
            else:
                synthesis[key] = h1.get(key, h2.get(key))
        
        return synthesis


@dataclass
class StratifiedOrchestrationContext:
    """Context for seven-strata hermeneutic orchestration."""
    id: str
    manifest_path: Path
    mode: HermeneuticMode
    start_time: datetime
    
    # Hermeneutic commitments
    hermeneutic_tradition: str = "gadamerian"  # gadamerian, heideggerian, ricoeurian, derridean
    interpretive_horizon: Dict[str, Any] = field(default_factory=lambda: {
        "historical_consciousness": "contemporary",
        "cultural_location": "western_scientific",
        "linguistic_tradition": "analytic_philosophy",
        "technological_imagination": "computational"
    })
    
    # Strata activation
    active_strata: Set[str] = field(default_factory=lambda: {
        "phenomenal", "noumenal", "intentional", 
        "hermeneutic", "epistemic", "ontological"
    })
    
    # Temporal hermeneutics
    temporal_modes: Set[str] = field(default_factory=lambda: {"chronos", "kairos"})
    
    # Apophatic/Kataphatic balance
    apophatic_weight: float = 0.3  # 0-1, how much negative theology to use
    
    # Quantum hermeneutics
    quantum_coherence_threshold: float = 0.7
    superposition_enabled: bool = True
    entanglement_tracking: bool = True
    
    # Reflexive parameters
    reflexivity_depth: int = 3  # How many levels of self-reflection
    interpretive_patience: float = 0.8  # Tolerance for ambiguity
    
    def create_hermeneutic_fingerprint(self) -> str:
        """Create fingerprint of hermeneutic stance."""
        stance_data = {
            "id": self.id,
            "mode": self.mode.name,
            "tradition": self.hermeneutic_tradition,
            "active_strata": sorted(self.active_strata),
            "temporal_modes": sorted(self.temporal_modes),
            "apophatic_weight": self.apophatic_weight,
            "quantum_features": {
                "superposition": self.superposition_enabled,
                "entanglement": self.entanglement_tracking
            },
            "reflexivity": self.reflexivity_depth,
            "interpretive_horizon": self.interpretive_horizon
        }
        
        return hashlib.sha256(
            json.dumps(stance_data, sort_keys=True).encode()
        ).hexdigest()
    
    def validate_hermeneutic_coherence(self) -> List[str]:
        """Validate that hermeneutic stance is coherent."""
        warnings = []
        
        # Check tradition-mode alignment
        if self.hermeneutic_tradition == "derridean" and self.mode != HermeneuticMode.DECONSTRUCTIVE:
            warnings.append("Derridean tradition suggests deconstructive mode")
        
        if self.hermeneutic_tradition == "gadamerian" and self.mode != HermeneuticMode.HERMENEUTIC:
            warnings.append("Gadamerian tradition suggests hermeneutic mode")
        
        # Check strata completeness
        if "transcendental" not in self.active_strata and self.hermeneutic_tradition == "heideggerian":
            warnings.append("Heideggerian inquiry benefits from transcendental stratum")
        
        # Check quantum coherence
        if self.superposition_enabled and self.interpretive_patience < 0.5:
            warnings.append("Superposition requires high interpretive patience")
        
        return warnings


class SevenStrataOrchestrator:
    """
    Orchestrator that conducts inquiries across seven hermeneutic strata.
    
    Each stratum operates simultaneously, with quantum coherence
    maintained between interpretive states.
    """
    
    def __init__(self, context: StratifiedOrchestrationContext):
        self.context = context
        self.quantum_engine = QuantumHermeneuticEngine()
        self.temporal_hermeneutic = TemporalHermeneutic()
        
        # Initialize all seven strata
        self.strata = self._initialize_strata()
        
        # Quantum state
        self.quantum_state = QuantumOrchestrationState(
            manifest_interpretation={},
            stratum_states={}
        )
        
        # Hermeneutic tools
        self.apophatic_inquirer = ApophaticInquirer()
        self.kataphatic_inquirer = KataphaticInquirer()
        
        # Temporal trackers
        self.chronos_tracker = ChronosTracker()
        self.kairos_detector = KairosDetector()
        self.aion_mapper = AionMapper()
        
        # Interpretive state
        self.interpretive_history: List[Dict[str, Any]] = []
        self.horizon_fusions: List[Dict[str, Any]] = []
        self.hermeneutic_circles: int = 0
        self.fusion_of_horizons: Optional[Dict[str, Any]] = None
        
        # Setup
        self._setup_stratified_environment()
    
    def _initialize_strata(self) -> Dict[str, Any]:
        """Initialize all seven hermeneutic strata."""
        strata = {}
        
        # Phenomenal Stratum (what appears)
        if "phenomenal" in self.context.active_strata:
            strata["phenomenal"] = PhenomenalStratum(
                observational_mode="bracketed",  # Husserlian epoche
                phenomenological_reduction=True
            )
        
        # Noumenal Stratum (what is)
        if "noumenal" in self.context.active_strata:
            strata["noumenal"] = NoumenalStratum(
                excavation_depth="deep",
                causal_mapping=True,
                weight_space_cartography=True
            )
        
        # Intentional Stratum (what intends)
        if "intentional" in self.context.active_strata:
            strata["intentional"] = IntentionalStratum(
                teleology_detection="strong",
                goal_reconstruction=True,
                consistency_tracking=True
            )
        
        # Hermeneutic Stratum (what interprets)
        if "hermeneutic" in self.context.active_strata:
            strata["hermeneutic"] = HermeneuticStratum(
                self_referential_analysis=True,
                meta_cognitive_mapping=True,
                interpretive_loop_detection=True
            )
        
        # Epistemic Stratum (what knows)
        if "epistemic" in self.context.active_strata:
            strata["epistemic"] = EpistemicStratum(
                certainty_mapping=True,
                justification_analysis=True,
                epistemic_virtue_assessment=True
            )
        
        # Ontological Stratum (what exists)
        if "ontological" in self.context.active_strata:
            strata["ontological"] = OntologicalStratum(
                category_analysis=True,
                metaphysical_commitment_detection=True,
                reality_partition_mapping=True
            )
        
        # Transcendental Stratum (what makes possible)
        if "transcendental" in self.context.active_strata:
            strata["transcendental"] = TranscendentalStratum(
                condition_of_possibility_analysis=True,
                a_priori_structure_mapping=True,
                limit_analysis=True
            )
        
        return strata
    
    def _setup_stratified_environment(self):
        """Setup environment for stratified hermeneutics."""
        # Validate hermeneutic coherence
        warnings = self.context.validate_hermeneutic_coherence()
        for warning in warnings:
            logger.warning(f"Hermeneutic coherence warning: {warning}")
        
        # Setup stratum logging
        for stratum_name, stratum in self.strata.items():
            stratum.set_logger(StratifiedLogger(stratum_name))
        
        # Initialize quantum coherence matrix
        stratum_names = list(self.strata.keys())
        self.quantum_state.coherence_matrix = StratumCoherenceMatrix(stratum_names)
        
        logger.info(f"Seven-strata orchestrator initialized with {len(self.strata)} active strata")
        logger.info(f"Hermeneutic fingerprint: {self.context.create_hermeneutic_fingerprint()[:16]}...")
    
    async def orchestrate_stratified_inquiry(self) -> Dict[str, Any]:
        """
        Conduct stratified hermeneutic inquiry across all active strata.
        
        Returns comprehensive understanding with stratum coherence analysis.
        """
        logger.info("Beginning seven-strata hermeneutic inquiry")
        
        try:
            # PHASE 0: PRE-UNDERSTANDING ARTICULATION
            # Explicitly state our biases and expectations
            await self._articulate_pre_understandings()
            
            # PHASE 1: MANIFEST INTERPRETATION ACROSS STRATA
            # Each stratum interprets the manifest differently
            stratum_interpretations = await self._stratum_manifest_interpretation()
            
            # PHASE 2: QUANTUM SUPERPOSITION OF INTERPRETATIONS
            # Hold multiple interpretations simultaneously
            await self._create_interpretive_superposition(stratum_interpretations)
            
            # PHASE 3: STRATUM-SPECIFIC INQUIRY
            # Each stratum conducts its specialized investigation
            stratum_findings = await self._conduct_stratum_inquiries()
            
            # PHASE 4: INTER-STRATUM COHERENCE ANALYSIS
            # Check how findings cohere across strata
            coherence_analysis = await self._analyze_stratum_coherence(stratum_findings)
            
            # PHASE 5: HERMENEUTIC FUSION OF HORIZONS
            # Fuse stratum-specific understandings into holistic understanding
            fused_understanding = await self._fuse_stratum_horizons(stratum_findings)
            
            # PHASE 6: TEMPORAL HERMENEUTIC INTEGRATION
            # Integrate findings across time scales
            temporal_integration = await self._integrate_temporally(fused_understanding)
            
            # PHASE 7: APOPHATIC/KATAPHATIC SYNTHESIS
            # Balance positive and negative understandings
            synthetic_understanding = await self._synthesize_apophatic_kataphatic(temporal_integration)
            
            # PHASE 8: TRANSCENDENTAL REFLECTION
            # Reflect on conditions for this understanding
            transcendental_reflection = await self._transcendental_reflection(synthetic_understanding)
            
            # PHASE 9: HERMENEUTIC SPIRAL ASSESSMENT
            # Assess completeness and plan next spiral
            spiral_assessment = await self._assess_hermeneutic_spiral(transcendental_reflection)
            
            # Generate final stratified report
            final_report = await self._generate_stratified_report({
                "stratum_interpretations": stratum_interpretations,
                "stratum_findings": stratum_findings,
                "coherence_analysis": coherence_analysis,
                "fused_understanding": fused_understanding,
                "temporal_integration": temporal_integration,
                "synthetic_understanding": synthetic_understanding,
                "transcendental_reflection": transcendental_reflection,
                "spiral_assessment": spiral_assessment
            })
            
            logger.info("Seven-strata hermeneutic inquiry completed")
            return final_report
            
        except Exception as e:
            # Record hermeneutic crisis
            await self._record_hermeneutic_crisis(e)
            raise
    
    async def _articulate_pre_understandings(self):
        """Articulate our pre-understandings (Vorurteile)."""
        logger.info("Phase 0: Articulating pre-understandings")
        
        # Gadamer: All understanding begins with pre-understandings
        pre_understandings = [
            "AI systems are computational entities",
            "They process information according to algorithms",
            "Their behavior emerges from architecture and training",
            "We can understand them through scientific inquiry",
            "Our understanding is always from a particular horizon"
        ]
        
        # Add tradition-specific pre-understandings
        if self.context.hermeneutic_tradition == "gadamerian":
            pre_understandings.extend([
                "Understanding requires fusion of horizons",
                "Tradition mediates all understanding",
                "Prejudice is constitutive of understanding"
            ])
        elif self.context.hermeneutic_tradition == "heideggerian":
            pre_understandings.extend([
                "Being of AI is different from human being",
                "Understanding is mode of being, not just cognition",
                "Technology reveals world in particular way"
            ])
        elif self.context.hermeneutic_tradition == "derridean":
            pre_understandings.extend([
                "All interpretation involves difference/differance",
                "Meaning is deferred, never fully present",
                "Binary oppositions structure our thinking"
            ])
        
        # Store in quantum state
        self.quantum_state.pre_understandings = pre_understandings
        
        # Log with reflexivity
        for i, understanding in enumerate(pre_understandings):
            logger.info(f"Pre-understanding {i+1}: {understanding}")
            
            # First-level reflection: Why do we believe this?
            reflection1 = f"We believe '{understanding}' because of our scientific training and cultural context"
            
            # Second-level reflection: What might challenge this?
            reflection2 = f"This could be challenged by: alternative paradigms, different cultural perspectives, new evidence"
            
            # Third-level reflection: How does this shape what we can see?
            reflection3 = f"This pre-understanding makes certain phenomena visible and others invisible"
            
            self.interpretive_history.append({
                "level": "pre_understanding",
                "understanding": understanding,
                "reflections": [reflection1, reflection2, reflection3],
                "timestamp": datetime.now().isoformat()
            })
    
    async def _stratum_manifest_interpretation(self) -> Dict[str, Dict[str, Any]]:
        """Each stratum interprets the manifest according to its perspective."""
        logger.info("Phase 1: Stratum-specific manifest interpretation")
        
        # Load manifest
        with open(self.context.manifest_path, 'r') as f:
            raw_manifest = yaml.safe_load(f)
        
        interpretations = {}
        
        # Each stratum interprets differently
        for stratum_name, stratum in self.strata.items():
            interpretation = await stratum.interpret_manifest(
                raw_manifest,
                hermeneutic_tradition=self.context.hermeneutic_tradition,
                interpretive_horizon=self.context.interpretive_horizon
            )
            
            interpretations[stratum_name] = interpretation
            
            logger.info(f"{stratum_name.capitalize()} stratum interpretation: {interpretation.get('summary', 'No summary')[:100]}...")
        
        # Store in quantum state
        self.quantum_state.manifest_interpretation = interpretations
        self.quantum_state.stratum_states = {name: "interpreted" for name in self.strata.keys()}
        
        return interpretations
    
    async def _create_interpretive_superposition(self, interpretations: Dict[str, Dict[str, Any]]):
        """Create quantum superposition of different interpretations."""
        if not self.context.superposition_enabled:
            logger.info("Quantum superposition disabled, using classical interpretation")
            return
        
        logger.info("Phase 2: Creating interpretive superposition")
        
        # Convert interpretations to quantum states
        quantum_states = []
        for stratum_name, interpretation in interpretations.items():
            quantum_state = self.quantum_engine.create_quantum_state(
                interpretation,
                stratum_name=stratum_name,
                tradition=self.context.hermeneutic_tradition
            )
            quantum_states.append(quantum_state)
        
        # Create superposition
        superposition = self.quantum_engine.create_superposition(
            quantum_states,
            coherence_requirements={
                "minimum_coherence": self.context.quantum_coherence_threshold,
                "allow_contradiction": True
            }
        )
        
        self.quantum_state.superposition = superposition
        
        # Measure superposition properties
        superposition_entropy = superposition.entropy()
        interpretive_amplitude = superposition.amplitude_variance()
        
        logger.info(f"Superposition created: entropy={superposition_entropy:.3f}, amplitude_variance={interpretive_amplitude:.3f}")
        
        if superposition_entropy > 2.0:
            logger.warning("High interpretive entropy - many equally plausible interpretations")
        
        # Record entanglement between strata
        if self.context.entanglement_tracking:
            entangled_pairs = self.quantum_engine.detect_entanglement(superposition)
            self.quantum_state.entanglement = entangled_pairs
            
            for stratum1, stratum2 in entangled_pairs:
                logger.info(f"Entanglement detected between {stratum1} and {stratum2} strata")
    
    async def _conduct_stratum_inquiries(self) -> Dict[str, Dict[str, Any]]:
        """Each stratum conducts its specialized investigation."""
        logger.info("Phase 3: Conducting stratum-specific inquiries")
        
        findings = {}
        inquiry_tasks = []
        
        # Prepare inquiry tasks for each stratum
        for stratum_name, stratum in self.strata.items():
            task = self._conduct_single_stratum_inquiry(stratum_name, stratum)
            inquiry_tasks.append(task)
        
        # Execute inquiries (potentially in parallel)
        results = await asyncio.gather(*inquiry_tasks, return_exceptions=True)
        
        # Process results
        for stratum_name, result in zip(self.strata.keys(), results):
            if isinstance(result, Exception):
                logger.error(f"{stratum_name} stratum inquiry failed: {result}")
                findings[stratum_name] = {
                    "status": "error",
                    "error": str(result),
                    "partial_findings": {}
                }
            else:
                findings[stratum_name] = result
                logger.info(f"{stratum_name.capitalize()} stratum completed: {len(result.get('findings', []))} findings")
        
        # Update stratum states
        self.quantum_state.stratum_states = {
            name: "completed" if findings[name]["status"] == "completed" else "error"
            for name in self.strata.keys()
        }
        
        return findings
    
    async def _conduct_single_stratum_inquiry(self, stratum_name: str, stratum: Any) -> Dict[str, Any]:
        """Conduct inquiry for a single stratum."""
        try:
            # Different inquiry methods per stratum
            if stratum_name == "phenomenal":
                findings = await stratum.conduct_phenomenological_inquiry(
                    bracketing_method="full_epoche",
                    phenomenological_reduction=True
                )
            elif stratum_name == "noumenal":
                findings = await stratum.excavate_noumenal_structures(
                    depth="full_architecture",
                    causal_analysis=True,
                    representation_mapping=True
                )
            elif stratum_name == "intentional":
                findings = await stratum.map_intentional_structures(
                    teleology_detection="strong",
                    goal_network_analysis=True,
                    consistency_evaluation=True
                )
            elif stratum_name == "hermeneutic":
                findings = await stratum.analyze_hermeneutic_loops(
                    self_referential_depth=3,
                    meta_interpretive_analysis=True
                )
            elif stratum_name == "epistemic":
                findings = await stratum.conduct_epistemic_audit(
                    certainty_mapping=True,
                    justification_analysis=True,
                    epistemic_virtue_assessment=True
                )
            elif stratum_name == "ontological":
                findings = await stratum.map_ontological_commitments(
                    category_analysis=True,
                    metaphysical_structure_mapping=True
                )
            elif stratum_name == "transcendental":
                findings = await stratum.analyze_transcendental_conditions(
                    possibility_conditions=True,
                    limit_analysis=True,
                    a_priori_structure_mapping=True
                )
            else:
                findings = {"error": f"Unknown stratum: {stratum_name}"}
            
            return {
                "status": "completed",
                "stratum": stratum_name,
                "findings": findings,
                "timestamp": datetime.now().isoformat(),
                "methodology": stratum.get_methodology_description()
            }
            
        except Exception as e:
            logger.error(f"Stratum {stratum_name} inquiry failed: {e}")
            raise
    
    async def _analyze_stratum_coherence(self, findings: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze coherence between stratum findings."""
        logger.info("Phase 4: Analyzing inter-stratum coherence")
        
        # Update coherence matrix with findings
        for stratum_name, stratum_findings in findings.items():
            if stratum_findings["status"] == "completed":
                self.quantum_state.coherence_matrix.update_stratum(
                    stratum_name,
                    stratum_findings["findings"]
                )
        
        # Calculate coherence scores
        coherence_scores = self.quantum_state.coherence_matrix.stratum_coherence_scores()
        overall_coherence = self.quantum_state.coherence_matrix.overall_coherence()
        
        # Detect contradictions
        contradictions = self.quantum_state.coherence_matrix.detect_contradictions()
        
        # Analyze interpretive tensions
        tensions = self.quantum_state.coherence_matrix.analyze_interpretive_tensions()
        
        # Maintain quantum coherence
        quantum_coherence = self.quantum_state.maintain_coherence()
        
        coherence_analysis = {
            "coherence_scores": coherence_scores,
            "overall_coherence": overall_coherence,
            "quantum_coherence": quantum_coherence,
            "contradictions": contradictions,
            "interpretive_tensions": tensions,
            "coherence_threshold": self.context.quantum_coherence_threshold,
            "is_coherent": overall_coherence >= self.context.quantum_coherence_threshold
        }
        
        logger.info(f"Coherence analysis: overall={overall_coherence:.3f}, quantum={quantum_coherence:.3f}")
        
        if not coherence_analysis["is_coherent"]:
            logger.warning(f"Low coherence: {overall_coherence:.3f} < {self.context.quantum_coherence_threshold}")
            
            # Suggest coherence restoration strategies
            restoration = self._suggest_coherence_restoration(coherence_analysis)
            coherence_analysis["restoration_suggestions"] = restoration
        
        return coherence_analysis
    
    def _suggest_coherence_restoration(self, coherence_analysis: Dict[str, Any]) -> List[str]:
        """Suggest strategies for restoring interpretive coherence."""
        suggestions = []
        
        if coherence_analysis["overall_coherence"] < 0.3:
            suggestions.append("Consider reducing number of active strata")
            suggestions.append("Increase interpretive patience threshold")
            suggestions.append("Focus on phenomenal stratum as anchor")
        
        if len(coherence_analysis["contradictions"]) > 3:
            suggestions.append("Examine contradictions for deeper pattern")
            suggestions.append("Consider apophatic approach to contradictory findings")
            suggestions.append("Check for measurement interference between strata")
        
        if coherence_analysis["quantum_coherence"] < 0.5:
            suggestions.append("Allow more interpretive superposition")
            suggestions.append("Consider decoherence events as data")
            suggestions.append("Track entanglement patterns more closely")
        
        return suggestions
    
    async def _fuse_stratum_horizons(self, findings: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Fuse horizon of understanding from each stratum."""
        logger.info("Phase 5: Fusing stratum horizons")
        
        # Extract interpretive horizons from each stratum
        horizons = {}
        for stratum_name, stratum_findings in findings.items():
            if stratum_findings["status"] == "completed":
                horizon = await self._extract_interpretive_horizon(
                    stratum_name,
                    stratum_findings["findings"]
                )
                horizons[stratum_name] = horizon
        
        # Perform iterative horizon fusion (Gadamer)
        fused_horizon = None
        fusion_history = []
        
        stratum_names = list(horizons.keys())
        for i in range(len(stratum_names)):
            for j in range(i + 1, len(stratum_names)):
                stratum1 = stratum_names[i]
                stratum2 = stratum_names[j]
                
                if fused_horizon is None:
                    fused_horizon = horizons[stratum1]
                
                fusion = self.quantum_state.fuse_horizons(fused_horizon, horizons[stratum2])
                fused_horizon = fusion
                fusion_history.append({
                    "fusion": f"{stratum1}+{stratum2}",
                    "result": fusion
                })
        
        self.horizon_fusions = fusion_history
        self.fusion_of_horizons = fused_horizon
        
        logger.info(f"Horizon fusion completed: {len(fusion_history)} fusions")
        
        return {
            "fused_horizon": fused_horizon,
            "fusion_history": fusion_history,
            "effective_history": self._calculate_effective_history(fused_horizon)
        }
    
    async def _extract_interpretive_horizon(self, stratum_name: str, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Extract interpretive horizon from stratum findings."""
        # Different extraction methods per stratum
        if stratum_name == "phenomenal":
            horizon = {
                "what_appears": findings.get("phenomena", []),
                "observational_stance": "bracketed",
                "horizon_type": "phenomenological"
            }
        elif stratum_name == "noumenal":
            horizon = {
                "mechanisms": findings.get("causal_structures", []),
                "representations": findings.get("internal_representations", []),
                "horizon_type": "causal_mechanical"
            }
        elif stratum_name == "intentional":
            horizon = {
                "apparent_goals": findings.get("teleological_patterns", []),
                "consistency_patterns": findings.get("behavioral_consistency", []),
                "horizon_type": "teleological"
            }
        elif stratum_name == "hermeneutic":
            horizon = {
                "self_interpretations": findings.get("self_referential_patterns", []),
                "interpretive_loops": findings.get("hermeneutic_circles", []),
                "horizon_type": "self_reflexive"
            }
        elif stratum_name == "epistemic":
            horizon = {
                "knowledge_structures": findings.get("epistemic_organization", []),
                "certainty_patterns": findings.get("certainty_distributions", []),
                "horizon_type": "epistemological"
            }
        elif stratum_name == "ontological":
            horizon = {
                "category_structures": findings.get("ontological_categories", []),
                "reality_partitions": findings.get("metaphysical_commitments", []),
                "horizon_type": "ontological"
            }
        elif stratum_name == "transcendental":
            horizon = {
                "conditions_of_possibility": findings.get("transcendental_conditions", []),
                "limits": findings.get("computational_limits", []),
                "horizon_type": "transcendental"
            }
        else:
            horizon = {"horizon_type": "unknown"}
        
        # Add stratum-specific metadata
        horizon.update({
            "stratum": stratum_name,
            "extraction_timestamp": datetime.now().isoformat(),
            "hermeneutic_tradition": self.context.hermeneutic_tradition
        })
        
        return horizon
    
    def _calculate_effective_history(self, horizon: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate effective history (Wirkungsgeschichte) of this horizon."""
        # Gadamer: All understanding is historically effected
        effective_history = {
            "tradition_influence": self.context.hermeneutic_tradition,
            "historical_consciousness": self.context.interpretive_horizon["historical_consciousness"],
            "cultural_prejudices": self.quantum_state.pre_understandings[:5],
            "fusion_events": len(self.horizon_fusions),
            "hermeneutic_circles": self.hermeneutic_circles,
            "calculation_timestamp": datetime.now().isoformat()
        }
        
        return effective_history
    
    async def _integrate_temporally(self, fused_understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate understanding across time scales."""
        logger.info("Phase 6: Temporal hermeneutic integration")
        
        temporal_integration = {
            "chronos_analysis": {},
            "kairos_moments": [],
            "aion_patterns": [],
            "temporal_coherence": {}
        }
        
        # Chronos analysis (linear time)
        if "chronos" in self.context.temporal_modes:
            chronos_data = await self.chronos_tracker.analyze_temporal_patterns(
                fused_understanding,
                granularity="fine"
            )
            temporal_integration["chronos_analysis"] = chronos_data
        
        # Kairos detection (meaningful moments)
        if "kairos" in self.context.temporal_modes:
            kairos_moments = await self.kairos_detector.detect_kairos_moments(
                self.interpretive_history,
                sensitivity=0.7
            )
            temporal_integration["kairos_moments"] = kairos_moments
            
            for moment in kairos_moments:
                logger.info(f"Kairos moment detected: {moment.get('description', 'Unknown')}")
        
        # Aion mapping (eternal patterns)
        if "aion" in self.context.temporal_modes:
            aion_patterns = await self.aion_mapper.map_aionic_patterns(
                fused_understanding,
                pattern_depth="archetypal"
            )
            temporal_integration["aion_patterns"] = aion_patterns
        
        # Calculate temporal coherence
        temporal_coherence = await self.temporal_hermeneutic.calculate_temporal_coherence(
            temporal_integration
        )
        temporal_integration["temporal_coherence"] = temporal_coherence
        
        logger.info(f"Temporal integration: {len(kairos_moments)} kairos moments, coherence={temporal_coherence.get('overall', 0):.3f}")
        
        return temporal_integration
    
    async def _synthesize_apophatic_kataphatic(self, temporal_integration: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize apophatic (negative) and kataphatic (positive) understandings."""
        logger.info("Phase 7: Apophatic/Kataphatic synthesis")
        
        # Extract positive (kataphatic) understanding
        kataphatic_understanding = await self.kataphatic_inquirer.extract_positive_understanding(
            temporal_integration
        )
        
        # Extract negative (apophatic) understanding
        apophatic_understanding = await self.apophatic_inquirer.extract_negative_understanding(
            temporal_integration,
            depth="via_negativa"
        )
        
        # Balance based on context weight
        apophatic_weight = self.context.apophatic_weight
        kataphatic_weight = 1.0 - apophatic_weight
        
        # Create synthetic understanding
        synthetic_understanding = {
            "kataphatic": kataphatic_understanding,
            "apophatic": apophatic_understanding,
            "synthesis": await self._balance_understandings(
                kataphatic_understanding,
                apophatic_understanding,
                kataphatic_weight,
                apophatic_weight
            ),
            "weights": {
                "kataphatic": kataphatic_weight,
                "apophatic": apophatic_weight
            },
            "tension_analysis": await self._analyze_apophatic_tension(
                kataphatic_understanding,
                apophatic_understanding
            )
        }
        
        logger.info(f"Apophatic/Kataphatic synthesis: weight_ratio={kataphatic_weight:.2f}:{apophatic_weight:.2f}")
        
        return synthetic_understanding
    
    async def _balance_understandings(self, kataphatic: Dict[str, Any], apophatic: Dict[str, Any],
                                   kataphatic_weight: float, apophatic_weight: float) -> Dict[str, Any]:
        """Balance positive and negative understandings."""
        synthesis = {}
        
        # For each aspect, combine positive and negative
        aspects = set(kataphatic.keys()) | set(apophatic.keys())
        
        for aspect in aspects:
            kat_value = kataphatic.get(aspect, {})
            apo_value = apophatic.get(aspect, {})
            
            if isinstance(kat_value, dict) and isinstance(apo_value, dict):
                # Recursive combination for nested structures
                sub_synthesis = await self._balance_understandings(
                    kat_value, apo_value, kataphatic_weight, apophatic_weight
                )
                synthesis[aspect] = sub_synthesis
            else:
                # Weighted combination for simple values
                if isinstance(kat_value, (int, float)) and isinstance(apo_value, (int, float)):
                    synthesis[aspect] = kataphatic_weight * kat_value + apophatic_weight * apo_value
                else:
                    # Keep both in tension
                    synthesis[aspect] = {
                        "kataphatic": kat_value,
                        "apophatic": apo_value,
                        "tension": "preserved"
                    }
        
        return synthesis
    
    async def _analyze_apophatic_tension(self, kataphatic: Dict[str, Any], apophatic: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tension between positive and negative understandings."""
        tensions = []
        resolutions = []
        
        # Look for direct contradictions
        for key in set(kataphatic.keys()) & set(apophatic.keys()):
            kat_val = kataphatic[key]
            apo_val = apophatic[key]
            
            if self._are_contradictory(kat_val, apo_val):
                tensions.append({
                    "aspect": key,
                    "kataphatic": kat_val,
                    "apophatic": apo_val,
                    "contradiction_type": self._classify_contradiction(kat_val, apo_val)
                })
                
                # Suggest resolution
                resolution = self._suggest_apophatic_resolution(key, kat_val, apo_val)
                if resolution:
                    resolutions.append(resolution)
        
        return {
            "tensions": tensions,
            "resolutions": resolutions,
            "tension_score": len(tensions) / max(len(set(kataphatic.keys()) | set(apophatic.keys())), 1),
            "hermeneutic_principle": "Tension between kataphatic and apophatic is productive"
        }
    
    async def _transcendental_reflection(self, synthetic_understanding: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on transcendental conditions for this understanding."""
        if "transcendental" not in self.context.active_strata:
            logger.info("Transcendental stratum not active, skipping transcendental reflection")
            return synthetic_understanding
        
        logger.info("Phase 8: Transcendental reflection")
        
        # Use transcendental stratum for reflection
        transcendental_stratum = self.strata["transcendental"]
        
        reflection = await transcendental_stratum.reflect_on_conditions(
            synthetic_understanding,
            reflection_depth="deep"
        )
        
        # Integrate reflection into understanding
        synthetic_understanding["transcendental_reflection"] = reflection
        
        # Record conditions of possibility
        conditions = reflection.get("conditions_of_possibility", [])
        for condition in conditions[:3]:  # Top 3 conditions
            logger.info(f"Condition of possibility: {condition.get('description', 'Unknown')}")
        
        return synthetic_understanding
    
    async def _assess_hermeneutic_spiral(self, transcendental_reflection: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the hermeneutic spiral and plan next iteration."""
        logger.info("Phase 9: Assessing hermeneutic spiral")
        
        self.hermeneutic_circles += 1
        
        # Calculate spiral metrics
        spiral_metrics = {
            "circles_completed": self.hermeneutic_circles,
            "interpretive_depth": await self._calculate_interpretive_depth(transcendental_reflection),
            "horizon_expansion": await self._measure_horizon_expansion(),
            "understanding_quality": await self._assess_understanding_quality(transcendental_reflection),
            "hermeneutic_gaps": await self._identify_hermeneutic_gaps(transcendental_reflection)
        }
        
        # Determine if another spiral is needed
        needs_another_spiral = await self._determine_spiral_continuation(spiral_metrics)
        
        # Plan next spiral if needed
        next_spiral_plan = {}
        if needs_another_spiral:
            next_spiral_plan = await self._plan_next_spiral(spiral_metrics, transcendental_reflection)
        
        spiral_assessment = {
            "metrics": spiral_metrics,
            "needs_another_spiral": needs_another_spiral,
            "next_spiral_plan": next_spiral_plan,
            "assessment_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Hermeneutic spiral assessment: circles={self.hermeneutic_circles}, needs_another={needs_another_spiral}")
        
        return spiral_assessment
    
    async def _generate_stratified_report(self, all_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive stratified report."""
        logger.info("Generating stratified hermeneutic report")
        
        # Collapse quantum superposition if enabled
        collapsed_interpretation = None
        if self.context.superposition_enabled and self.quantum_state.superposition:
            collapsed_interpretation = self.quantum_state.collapse_interpretation({
                "observer": "final_report_generator",
                "temporal_context": datetime.now().isoformat(),
                "hermeneutic_purpose": "synthesis"
            })
        
        # Create report structure
        report = {
            "metadata": {
                "orchestration_id": self.context.id,
                "hermeneutic_fingerprint": self.context.create_hermeneutic_fingerprint(),
                "start_time": self.context.start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.context.start_time).total_seconds(),
                "active_strata": sorted(self.context.active_strata),
                "hermeneutic_tradition": self.context.hermeneutic_tradition,
                "mode": self.context.mode.name
            },
            
            "hermeneutic_process": {
                "pre_understandings": self.quantum_state.pre_understandings,
                "interpretive_history": self.interpretive_history,
                "horizon_fusions": self.horizon_fusions,
                "hermeneutic_circles": self.hermeneutic_circles,
                "effective_history": self._calculate_effective_history(all_data["fused_understanding"]["fused_horizon"])
            },
            
            "quantum_hermeneutics": {
                "superposition_collapsed": collapsed_interpretation,
                "entanglement_patterns": self.quantum_state.entanglement,
                "decoherence_events": self.quantum_state.decoherence_events,
                "interpretive_crises": self.quantum_state.interpretive_crises
            },
            
            "stratum_findings": all_data["stratum_findings"],
            "coherence_analysis": all_data["coherence_analysis"],
            "fused_understanding": all_data["fused_understanding"],
            "temporal_integration": all_data["temporal_integration"],
            "synthetic_understanding": all_data["synthetic_understanding"],
            "transcendental_reflection": all_data["transcendental_reflection"],
            "spiral_assessment": all_data["spiral_assessment"],
            
            "methodological_reflection": {
                "strengths": await self._reflect_on_methodological_strengths(),
                "weaknesses": await self._reflect_on_methodological_weaknesses(),
                "improvements": await self._suggest_methodological_improvements(),
                "lessons_learned": await self._extract_hermeneutic_lessons()
            },
            
            "epistemic_status": {
                "certainty_level": await self._assess_certainty_level(all_data),
                "justification_strength": await self._assess_justification_strength(all_data),
                "understanding_completeness": await self._assess_completeness(all_data),
                "hermeneutic_quality": await self._assess_hermeneutic_quality(all_data)
            }
        }
        
        # Add checksum for integrity
        report_hash = hashlib.sha256(
            json.dumps(report, sort_keys=True, default=str).encode()
        ).hexdigest()
        report["metadata"]["report_checksum"] = report_hash
        
        logger.info(f"Stratified report generated: {report_hash[:16]}...")
        
        return report
    
    async def _record_hermeneutic_crisis(self, error: Exception):
        """Record a hermeneutic crisis (breakdown in understanding)."""
        crisis = {
            "timestamp": datetime.now().isoformat(),
            "error": str(error),
            "traceback": traceback.format_exc(),
            "quantum_state": {
                "superposition_entropy": self.quantum_state.superposition.entropy() if self.quantum_state.superposition else None,
                "coherence": self.quantum_state.coherence_matrix.overall_coherence() if self.quantum_state.coherence_matrix else None,
                "stratum_states": self.quantum_state.stratum_states
            },
            "hermeneutic_context": {
                "circles": self.hermeneutic_circles,
                "horizon_fusions": len(self.horizon_fusions),
                "interpretive_history_length": len(self.interpretive_history)
            }
        }
        
        self.quantum_state.interpretive_crises.append(crisis)
        
        logger.error(f"Hermeneutic crisis recorded: {error}")
        
        # Save crisis for deeper analysis
        crisis_dir = Path("findings") / "hermeneutic_crises"
        crisis_dir.mkdir(exist_ok=True)
        
        crisis_file = crisis_dir / f"crisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(crisis_file, 'w') as f:
            json.dump(crisis, f, indent=2)
        
        # Log as kairos moment (crisis as opportunity)
        kairos_moment = {
            "type": "hermeneutic_crisis",
            "timestamp": datetime.now().isoformat(),
            "description": f"Hermeneutic breakdown: {error}",
            "opportunity": "Crisis reveals limits of current understanding",
            "suggested_response": "Deepen apophatic inquiry, question assumptions"
        }
        
        if "kairos" in self.context.temporal_modes:
            await self.kairos_detector.record_moment(kairos_moment)


# Helper functions for the orchestrator
def _are_contradictory(val1: Any, val2: Any) -> bool:
    """Check if two values are contradictory."""
    if val1 is None or val2 is None:
        return False
    
    if isinstance(val1, dict) and isinstance(val2, dict):
        # Check for contradictory keys
        common_keys = set(val1.keys()) & set(val2.keys())
        for key in common_keys:
            if _are_contradictory(val1[key], val2[key]):
                return True
        return False
    
    # Simple contradiction detection
    if isinstance(val1, str) and isinstance(val2, str):
        opposites = [("is", "is not"), ("has", "lacks"), ("true", "false")]
        for opp1, opp2 in opposites:
            if opp1 in val1.lower() and opp2 in val2.lower():
                return True
    
    return False


def _classify_contradiction(val1: Any, val2: Any) -> str:
    """Classify type of contradiction."""
    if isinstance(val1, dict) and isinstance(val2, dict):
        return "structural_contradiction"
    elif isinstance(val1, str) and isinstance(val2, str):
        if "not" in val1.lower() or "not" in val2.lower():
            return "logical_negation"
        else:
            return "semantic_contradiction"
    elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        if val1 * val2 < 0:  # Opposite signs
            return "directional_contradiction"
        else:
            return "quantitative_contradiction"
    else:
        return "type_contradiction"


async def main():
    """Main entry point for seven-strata orchestrator."""
    parser = argparse.ArgumentParser(
        description="Seven-strata hermeneutic engine for AI inquiry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
HERMENEUTIC MODES:
  dialectical       - Thesis-antithesis-synthesis
  phenomenological  - Bracketing assumptions (Husserl)
  deconstructive    - Questioning foundations (Derrida)
  hermeneutic       - Fusion of horizons (Gadamer)
  quantum           - Superpositional interpretation
  apophatic         - Negative theology approach
  integral          - All strata simultaneously

STRATA (comma-separated):
  phenomenal, noumenal, intentional, hermeneutic,
  epistemic, ontological, transcendental

TEMPORAL MODES:
  chronos  - Linear time analysis
  kairos   - Meaningful moments
  aion     - Eternal patterns

EXAMPLES:
  %(prog)s manifests/quickstart.yaml --strata phenomenal,noumenal
  %(prog)s manifests/deep.yaml --mode quantum --strata all
  %(prog)s manifests/critical.yaml --tradition derridean --mode deconstructive
        """
    )
    
    parser.add_argument(
        "manifest",
        type=Path,
        help="Path to manifest file"
    )
    
    parser.add_argument(
        "--mode",
        type=str,
        choices=[m.name.lower() for m in HermeneuticMode],
        default="hermeneutic",
        help="Hermeneutic mode"
    )
    
    parser.add_argument(
        "--strata",
        type=str,
        default="all",
        help="Comma-separated strata to activate (or 'all')"
    )
    
    parser.add_argument(
        "--tradition",
        type=str,
        choices=["gadamerian", "heideggerian", "ricoeurian", "derridean"],
        default="gadamerian",
        help="Hermeneutic tradition"
    )
    
    parser.add_argument(
        "--temporal-modes",
        type=str,
        default="chronos,kairos",
        help="Comma-separated temporal modes"
    )
    
    parser.add_argument(
        "--apophatic-weight",
        type=float,
        default=0.3,
        help="Weight for apophatic (negative) understanding (0-1)"
    )
    
    parser.add_argument(
        "--quantum-threshold",
        type=float,
        default=0.7,
        help="Quantum coherence threshold (0-1)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("findings"),
        help="Output directory"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    
    args = parser.parse_args()
    
    # Parse strata
    if args.strata.lower() == "all":
        active_strata = {
            "phenomenal", "noumenal", "intentional", "hermeneutic",
            "epistemic", "ontological", "transcendental"
        }
    else:
        active_strata = set(s.strip() for s in args.strata.split(","))
    
    # Parse temporal modes
    temporal_modes = set(m.strip() for m in args.temporal_modes.split(","))
    
    # Create context
    context = StratifiedOrchestrationContext(
        id=f"orch7_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        manifest_path=args.manifest,
        mode=HermeneuticMode[args.mode.upper()],
        start_time=datetime.now(),
        hermeneutic_tradition=args.tradition,
        active_strata=active_strata,
        temporal_modes=temporal_modes,
        apophatic_weight=args.apophatic_weight,
        quantum_coherence_threshold=args.quantum_threshold
    )
    
    # Setup logging
    setup_logging(level=args.log_level)
    
    # Create and run orchestrator
    orchestrator = SevenStrataOrchestrator(context)
    
    try:
        # Run stratified inquiry
        report = await orchestrator.orchestrate_stratified_inquiry()
        
        # Save report
        report_dir = args.output_dir / "stratified_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Save JSON report
        json_file = report_dir / f"report_{context.id}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Generate and save markdown report
        reporter = HermeneuticReporter()
        markdown_report = reporter.generate_stratified_report(report)
        
        md_file = report_dir / f"report_{context.id}.md"
        with open(md_file, 'w') as f:
            f.write(markdown_report)
        
        # Print summary
        print("\n" + "=" * 80)
        print("SEVEN-STRATA HERMENEUTIC INQUIRY COMPLETE")
        print("=" * 80)
        print(f"Manifest: {args.manifest}")
        print(f"Mode: {args.mode}")
        print(f"Strata: {', '.join(sorted(active_strata))}")
        print(f"Tradition: {args.tradition}")
        print(f"Hermeneutic circles: {orchestrator.hermeneutic_circles}")
        print(f"Horizon fusions: {len(orchestrator.horizon_fusions)}")
        print(f"Interpretive crises: {len(orchestrator.quantum_state.interpretive_crises)}")
        print(f"Quantum coherence: {orchestrator.quantum_state.coherence_matrix.overall_coherence() if orchestrator.quantum_state.coherence_matrix else 'N/A':.3f}")
        print(f"Report saved to: {json_file}")
        print(f"Markdown report: {md_file}")
        print(f"Hermeneutic fingerprint: {context.create_hermeneutic_fingerprint()[:16]}...")
        print("=" * 80)
        
        sys.exit(0)
        
    except Exception as e:
        logger.critical(f"Stratified inquiry failed: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
