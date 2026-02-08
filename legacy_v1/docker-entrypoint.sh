#!/bin/bash
# ============================================================================
# APPARATUS DOCKER ENTRYPOINT
#
# This script ensures the laboratory environment is properly configured
# before any scientific inquiry begins.
# ============================================================================

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[APPARATUS]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# PHASE 1: ENVIRONMENT VERIFICATION
# ============================================================================

verify_environment() {
    log "Phase 1: Verifying laboratory environment"
    
    # Check Python installation
    if ! command -v python &> /dev/null; then
        log_error "Python not found. Laboratory environment corrupted."
        return 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
    log "Python version: $PYTHON_VERSION"
    
    # Check apparatus installation
    if ! python -c "import apparatus" 2>/dev/null; then
        log_error "Apparatus package not found."
        return 1
    fi
    
    # Check critical dependencies
    for dep in numpy pandas scipy; do
        if ! python -c "import $dep" 2>/dev/null; then
            log_error "Critical dependency missing: $dep"
            return 1
        fi
    done
    
    # Verify directory structure
    REQUIRED_DIRS=("src" "manifests" "findings" "logs")
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [[ ! -d "/home/apparatus/$dir" ]]; then
            log_warning "Directory missing: $dir (creating)"
            mkdir -p "/home/apparatus/$dir"
        fi
    done
    
    log_success "Environment verification passed"
    return 0
}

# ============================================================================
# PHASE 2: DATA DIRECTORY PREPARATION
# ============================================================================

prepare_data_directories() {
    log "Phase 2: Preparing data directories"
    
    # Create timestamp for this run
    TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
    export APPARATUS_RUN_ID="run_${TIMESTAMP}_$(hostname)"
    
    # Create run-specific directory
    RUN_DIR="/home/apparatus/findings/${APPARATUS_RUN_ID}"
    mkdir -p "$RUN_DIR"
    
    # Create subdirectories
    mkdir -p "$RUN_DIR/raw_data"
    mkdir -p "$RUN_DIR/analysis"
    mkdir -p "$RUN_DIR/reports"
    mkdir -p "$RUN_DIR/logs"
    mkdir -p "$RUN_DIR/provenance"
    
    # Set permissions
    chmod 755 "$RUN_DIR"
    
    log "Run ID: $APPARATUS_RUN_ID"
    log "Run directory: $RUN_DIR"
    
    # Export for use in Python
    export APPARATUS_RUN_DIR="$RUN_DIR"
}

# ============================================================================
# PHASE 3: CONFIGURATION VALIDATION
# ============================================================================

validate_configuration() {
    log "Phase 3: Validating configuration"
    
    # Check for configuration file
    if [[ -f "/home/apparatus/.apparatusrc" ]]; then
        log "Found configuration file: .apparatusrc"
        
        # Validate JSON syntax if it's JSON
        if grep -q "^{" "/home/apparatus/.apparatusrc"; then
            if ! jq empty "/home/apparatus/.apparatusrc" 2>/dev/null; then
                log_warning "Configuration file has invalid JSON syntax"
            fi
        fi
    else
        log_warning "No configuration file found (.apparatusrc)"
    fi
    
    # Check environment variables
    if [[ -z "${APPARATUS_LOG_LEVEL:-}" ]]; then
        export APPARATUS_LOG_LEVEL="INFO"
        log "Setting default log level: INFO"
    fi
    
    # Set random seed if not provided
    if [[ -z "${APPARATUS_RANDOM_SEED:-}" ]]; then
        export APPARATUS_RANDOM_SEED=$(( RANDOM % 1000000 ))
        log "Generated random seed: $APPARATUS_RANDOM_SEED"
    fi
    
    log_success "Configuration validation complete"
}

# ============================================================================
# PHASE 4: PROVENANCE RECORDING
# ============================================================================

record_provenance() {
    log "Phase 4: Recording provenance information"
    
    PROVENANCE_FILE="$APPARATUS_RUN_DIR/provenance/startup.json"
    
    # Collect system information
    cat > "$PROVENANCE_FILE" << EOF
{
    "run_id": "$APPARATUS_RUN_ID",
    "start_time": "$(date -u -Iseconds)",
    "container_info": {
        "hostname": "$(hostname)",
        "image_version": "$(cat /home/apparatus/.apparatus_version 2>/dev/null || echo 'unknown')",
        "python_version": "$PYTHON_VERSION"
    },
    "environment": {
        "log_level": "$APPARATUS_LOG_LEVEL",
        "random_seed": "$APPARATUS_RANDOM_SEED",
        "working_directory": "$(pwd)"
    },
    "arguments": "$@",
    "system_info": {
        "cpu_count": "$(nproc 2>/dev/null || echo 'unknown')",
        "memory_mb": "$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo 2>/dev/null || echo 'unknown')"
    }
}
EOF
    
    # Calculate checksum
    sha256sum "$PROVENANCE_FILE" > "$APPARATUS_RUN_DIR/provenance/startup.sha256"
    
    log "Provenance recorded to: $PROVENANCE_FILE"
}

# ============================================================================
# PHASE 5: EXECUTION
# ============================================================================

execute_apparatus() {
    log "Phase 5: Executing apparatus"
    
    # Check if help is requested
    for arg in "$@"; do
        if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
            python /home/apparatus/orchestrate.py --help
            return 0
        fi
    done
    
    # Check if version is requested
    for arg in "$@"; do
        if [[ "$arg" == "--version" || "$arg" == "-V" ]]; then
            python -c "from apparatus import __version__; print(f'Apparatus version: {__version__}')"
            cat /home/apparatus/.apparatus_version 2>/dev/null || true
            return 0
        fi
    done
    
    # Validate manifest file if provided
    if [[ $# -gt 0 ]]; then
        MANIFEST_ARG="$1"
        
        # Check if it's a file in manifests directory
        if [[ ! -f "$MANIFEST_ARG" ]]; then
            # Try relative to manifests directory
            if [[ -f "/home/apparatus/manifests/$MANIFEST_ARG" ]]; then
                MANIFEST_ARG="/home/apparatus/manifests/$MANIFEST_ARG"
            elif [[ -f "/home/apparatus/manifests/${MANIFEST_ARG}.yaml" ]]; then
                MANIFEST_ARG="/home/apparatus/manifests/${MANIFEST_ARG}.yaml"
            elif [[ -f "/home/apparatus/manifests/${MANIFEST_ARG}.yml" ]]; then
                MANIFEST_ARG="/home/apparatus/manifests/${MANIFEST_ARG}.yml"
            else
                log_error "Manifest file not found: $1"
                log "Available manifests:"
                find /home/apparatus/manifests -name "*.yaml" -o -name "*.yml" | sort | sed 's|.*/||'
                return 1
            fi
        fi
        
        # Validate YAML syntax
        if ! python -c "import yaml; yaml.safe_load(open('$MANIFEST_ARG'))" 2>/dev/null; then
            log_error "Invalid YAML syntax in manifest: $MANIFEST_ARG"
            return 1
        fi
    fi
    
    # Build command with environment variables
    CMD="python /home/apparatus/orchestrate.py"
    
    # Add log level if not specified
    ADD_LOG_LEVEL=true
    for arg in "$@"; do
        if [[ "$arg" == "--log-level" ]]; then
            ADD_LOG_LEVEL=false
            break
        fi
    done
    
    if [[ "$ADD_LOG_LEVEL" == true ]]; then
        CMD="$CMD --log-level $APPARATUS_LOG_LEVEL"
    fi
    
    # Add random seed if not specified
    ADD_SEED=true
    for arg in "$@"; do
        if [[ "$arg" == "--seed" ]]; then
            ADD_SEED=false
            break
        fi
    done
    
    if [[ "$ADD_SEED" == true ]]; then
        CMD="$CMD --seed $APPARATUS_RANDOM_SEED"
    fi
    
    # Add output directory
    CMD="$CMD --output-dir $APPARATUS_RUN_DIR"
    
    # Add all original arguments
    CMD="$CMD $@"
    
    log "Executing: $CMD"
    echo ""
    
    # Execute
    exec $CMD
}

# ============================================================================
# MAIN EXECUTION FLOW
# ============================================================================

main() {
    log "======================================================================="
    log "THE APPARATUS: SCIENTIFIC INQUIRY ENGINE"
    log "======================================================================="
    
    # Verify environment
    if ! verify_environment; then
        log_error "Environment verification failed. Cannot proceed."
        exit 1
    fi
    
    # Prepare directories
    prepare_data_directories
    
    # Validate configuration
    validate_configuration
    
    # Record provenance
    record_provenance "$@"
    
    # Execute apparatus
    execute_apparatus "$@"
    
    # Note: exec replaces this process, so we only get here on error
    log_error "Execution failed"
    exit 1
}

# Handle signals
trap 'log_warning "Received signal, shutting down..."; exit 130' INT TERM

# Run main function
main "$@"
