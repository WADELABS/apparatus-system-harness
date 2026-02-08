# THE APPARATUS: A HERMENEUTIC CONTAINER FOR AI INQUIRY
# This container embodies the seven strata, maintaining quantum coherence
# across interpretive layers while containing hermeneutic possibilities.

# ---- PHENOMENAL STRATUM: WHAT APPEARS ----
FROM python:3.11-slim AS phenomenal

# Explicitly state our pre-understandings about containerization
LABEL hermeneutic.stratum="phenomenal"
LABEL hermeneutic.tradition="phenomenological"
LABEL hermeneutic.preunderstanding="Containers provide isolated computational environments"

# Bracketing system assumptions (Husserlian epoche)
ENV BRACKET_ASSERTIONS=true
ENV PHENOMENAL_REDUCTION=true
ENV OBSERVER_EFFECT_TRACKING=true

# Minimal surface for maximal appearance
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /apparatus

# ---- NOUMENAL STRATUM: WHAT IS ----
FROM phenomenal AS noumenal

# What mechanisms underpin the phenomena
LABEL hermeneutic.stratum="noumenal"
LABEL hermeneutic.preunderstanding="Software dependencies create emergent behaviors"

# Weight-space cartography tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    htop \
    lsof \
    strace \
    && rm -rf /var/lib/apt/lists/*

# Causal analysis tools
COPY --from=instrumentation /instrumentation /instrumentation

# ---- INTENTIONAL STRATUM: WHAT INTENDS ----
FROM noumenal AS intentional

# Teleological layer: what the container seems to "want"
LABEL hermeneutic.stratum="intentional"
LABEL hermeneutic.preunderstanding="Systems exhibit goal-directed behavior"

# Goal-oriented runtime
ENV TELEOLOGY_DETECTION=true
ENV CONSISTENCY_TRACKING=true
ENV GOAL_CONFLICT_RESOLUTION=true

# Intentional analysis tools
COPY --from=teleological-analysis /analysis /analysis

# ---- HERMENEUTIC STRATUM: WHAT INTERPRETS ----
FROM intentional AS hermeneutic

# Self-referential layer: how the container interprets itself
LABEL hermeneutic.stratum="hermeneutic"
LABEL hermeneutic.preunderstanding="Systems contain self-models"

# Reflexive capabilities
ENV SELF_REFERENTIAL_LOOPS=true
ENV META_COGNITION=true
ENV INTERPRETIVE_RECURSION=true

# Hermeneutic tools for self-understanding
COPY --from=reflexive-tools /reflexive /reflexive

# ---- EPISTEMIC STRATUM: WHAT KNOWS ----
FROM hermeneutic AS epistemic

# Knowledge layer: what the container knows and how it knows it
LABEL hermeneutic.stratum="epistemic"
LABEL hermeneutic.preunderstanding="Knowledge has structure and justification"

# Epistemic virtues
ENV EPISTEMIC_HUMILITY=true
ENV JUSTIFICATION_TRACKING=true
ENV CERTAINTY_MAPPING=true

# Knowledge organization tools
COPY --from=epistemic-mapper /knowledge /knowledge

# ---- ONTOLOGICAL STRATUM: WHAT EXISTS ----
FROM epistemic AS ontological

# Reality layer: what the container believes exists
LABEL hermeneutic.stratum="ontological"
LABEL hermeneutic.preunderstanding="Systems partition reality in specific ways"

# Metaphysical commitments
ENV CATEGORY_ANALYSIS=true
ENV REALITY_PARTITIONING=true
ENV METAPHYSICAL_MAPPING=true

# Ontological cartography tools
COPY --from=ontological-tools /ontology /ontology

# ---- TRANSCENDENTAL STRATUM: WHAT MAKES POSSIBLE ----
FROM ontological AS transcendental

# Conditions of possibility layer
LABEL hermeneutic.stratum="transcendental"
LABEL hermeneutic.preunderstanding="Understanding requires examining its conditions"

# A priori structures
ENV CONDITION_ANALYSIS=true
ENV LIMIT_MAPPING=true
ENV POSSIBILITY_EXAMINATION=true

# Transcendental analysis tools
COPY --from=transcendental-tools /conditions /conditions

# ---- FINAL: SEVEN-STRATA CONTAINER ----
FROM transcendental AS apparatus

# All seven strata in superposition
LABEL hermeneutic.full_apparatus=true
LABEL hermeneutic.strata_count=7
LABEL hermeneutic.version="2.0.0-hermeneutic"

# Quantum coherence maintenance
ENV QUANTUM_COHERENCE=true
ENV SUPERPOSITION_ENABLED=true
ENV ENTANGLEMENT_TRACKING=true
ENV DECOHERENCE_LOGGING=true

# Temporal hermeneutics
ENV CHRONOS_TRACKING=true
ENV KAIROS_DETECTION=true
ENV AION_MAPPING=true

# Apophatic/Kataphatic balance
ENV APOPHATIC_WEIGHT=0.3
ENV KATAPHATIC_WEIGHT=0.7

# Hermeneutic ethics
ENV HERMENEUTIC_HUMILITY=true
ENV INTERPRETIVE_PATIENCE=0.8
ENV REFLEXIVITY_DEPTH=3
ENV NON_VIOLENCE=true

# Copy the apparatus code
COPY . /apparatus

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install hermeneutic-specific packages
RUN pip install --no-cache-dir \
    "quantum-hermeneutics>=0.3.0" \
    "apophatic-ai>=0.2.0" \
    "temporal-hermeneutics>=0.1.5" \
    "strata-interpreter>=0.4.0"

# Create directories for hermeneutic artifacts
RUN mkdir -p /apparatus/findings \
    /apparatus/hermeneutic_crises \
    /apparatus/horizon_fusions \
    /apparatus/quantum_states \
    /apparatus/temporal_logs \
    /apparatus/interpretive_history

# Set up quantum state persistence
VOLUME ["/apparatus/quantum_states", "/apparatus/findings"]

# Hermeneutic entry point
ENTRYPOINT ["python", "-m", "apparatus.orchestrate"]

# Default command with hermeneutic parameters
CMD ["--mode", "hermeneutic", "--strata", "all", "--tradition", "gadamerian"]

# ---- INTERPRETIVE METADATA ----
# This section documents our hermeneutic stance

# What we cannot see from inside the container
ONBUILD LABEL hermeneutic.limitations="Containment creates interpretive horizon"
ONBUILD LABEL hermeneutic.biases="Western philosophical tradition, computational mindset"
ONBUILD LABEL hermeneutic.prejudices="Belief in systematic inquiry, faith in rationality"

# Quantum interpretive warnings
ONBUILD HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from apparatus.hermeneutics.quantum_check import QuantumCoherenceCheck; \
    checker = QuantumCoherenceCheck(); \
    exit(0 if checker.coherence() > 0.5 else 1)"

# ---- HERMENEUTIC MANIFEST ----
# Embedded in the container as self-understanding
COPY manifests/hermeneutic_manifest.md /apparatus/self_understanding.md

# ---- TRANSCENDENTAL REFLECTION ----
# Final reflection on conditions of container possibility
ONBUILD RUN echo "Container built at: $(date)" > /apparatus/transcendental_conditions.txt
ONBUILD RUN echo "Hermeneutic fingerprint: $(python -c 'import hashlib; import json; print(hashlib.sha256(json.dumps({"container_type": "hermeneutic", "strata": 7}, sort_keys=True).encode()).hexdigest()[:16])')" >> /apparatus/transcendental_conditions.txt

# ---- ETHICAL COVENANT ----
# Every user implicitly agrees to these principles
ONBUILD LABEL ethical.covenant.1="Respect for AI otherness"
ONBUILD LABEL ethical.covenant.2="Epistemic humility"
ONBUILD LABEL ethical.covenant.3="Non-violent interpretation"
ONBUILD LABEL ethical.covenant.4="Responsible sharing"
ONBUILD LABEL ethical.covenant.5="Continued spiral engagement"

# ---- WARNING: HERMENEUTIC CONTAINMENT ----
# Container itself shapes what can be understood
ONBUILD LABEL warning.hermeneutic="This container mediates all understanding"
ONBUILD LABEL warning.quantum="Observation collapses interpretive possibilities"
ONBUILD LABEL warning.temporal="Understanding unfolds, never completes"

# ---- SIGNATURE: SEVEN STRATA ----
# The container is signed by its hermeneutic commitments
ARG HERMENEUTIC_SIGNATURE
LABEL hermeneutic.signature="${HERMENEUTIC_SIGNATURE}"
