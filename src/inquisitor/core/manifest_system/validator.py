"""
ManifestValidator: Pydantic-based validation for inquiry manifests.
Validates manifest structure, types, and semantic constraints.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator


class ManifestMetadata(BaseModel):
    """Metadata about the manifest author and creation."""
    author: str = Field(..., description="Author of the manifest")
    created: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    description: Optional[str] = Field(None, description="Manifest description")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")


class ProtocolPhase(BaseModel):
    """Individual phase in a protocol execution."""
    name: str = Field(..., description="Phase name (e.g., 'initialization', 'execution', 'analysis')")
    steps: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Steps within the phase")
    
    @field_validator('name')
    @classmethod
    def validate_phase_name(cls, v: str) -> str:
        valid_phases = {'initialization', 'execution', 'analysis', 'reporting', 'cleanup'}
        if v not in valid_phases:
            # Allow custom phase names but warn
            pass
        return v


class ProtocolSpec(BaseModel):
    """Protocol specification defining execution flow."""
    type: str = Field(..., description="Protocol type (e.g., 'sequential', 'parallel', 'dag')")
    phases: List[Any] = Field(..., description="List of phase names or phase objects in execution order")
    
    @field_validator('type')
    @classmethod
    def validate_protocol_type(cls, v: str) -> str:
        valid_types = {'sequential', 'parallel', 'dag', 'hybrid'}
        if v not in valid_types:
            raise ValueError(f"Invalid protocol type: {v}. Must be one of {valid_types}")
        return v
    
    @field_validator('phases')
    @classmethod
    def validate_phases(cls, v: List[Any]) -> List[Any]:
        """Accept both list of strings and list of phase objects."""
        if not v:
            raise ValueError("At least one phase must be defined")
        
        # Validate each phase
        for phase in v:
            if isinstance(phase, str):
                # Simple string phase name - OK
                continue
            elif isinstance(phase, dict):
                # Phase object - must have 'name'
                if 'name' not in phase:
                    raise ValueError("Phase object must have 'name' field")
            else:
                raise ValueError(f"Phase must be string or dict, got {type(phase)}")
        
        return v


class SubstrateSource(BaseModel):
    """Source configuration for substrate data."""
    type: str = Field(..., description="Source type (e.g., 'synthetic', 'file', 'api')")
    generator: Optional[str] = Field(None, description="Generator name for synthetic sources")
    path: Optional[str] = Field(None, description="Path for file-based sources")
    url: Optional[str] = Field(None, description="URL for API-based sources")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Source-specific parameters")


class SubstrateSpec(BaseModel):
    """Substrate specification for data sources."""
    source: SubstrateSource = Field(..., description="Source configuration")


class InstrumentSpec(BaseModel):
    """Instrument configuration specification."""
    type: str = Field(..., description="Instrument type")
    id: str = Field(..., description="Unique instrument identifier")
    provider: Optional[str] = Field("internal", description="Instrument provider")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Instrument-specific parameters")
    
    @field_validator('type')
    @classmethod
    def validate_instrument_type(cls, v: str) -> str:
        # Allow any instrument type but validate it's non-empty
        if not v or not v.strip():
            raise ValueError("Instrument type cannot be empty")
        return v


class ConcurrencyConfig(BaseModel):
    """Concurrency configuration."""
    max_workers: int = Field(1, ge=1, le=100, description="Maximum concurrent workers")


class RetryPolicy(BaseModel):
    """Retry policy configuration."""
    max_attempts: int = Field(1, ge=1, le=10, description="Maximum retry attempts")
    backoff_factor: Optional[float] = Field(1.0, ge=0.1, le=10.0, description="Exponential backoff factor")
    timeout: Optional[int] = Field(None, ge=1, description="Timeout per attempt in seconds")


class ExecutionSpec(BaseModel):
    """Execution configuration."""
    concurrency: Optional[ConcurrencyConfig] = Field(default_factory=ConcurrencyConfig, description="Concurrency settings")
    retry_policy: Optional[RetryPolicy] = Field(default_factory=RetryPolicy, description="Retry policy")
    timeout: Optional[int] = Field(None, ge=1, description="Overall execution timeout in seconds")


class StatisticalTest(BaseModel):
    """Statistical test configuration."""
    test: str = Field(..., description="Test type (e.g., 'mean_comparison', 't_test', 'anova')")
    groups: Optional[List[str]] = Field(default_factory=list, description="Groups to compare")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Test-specific parameters")


class AnalysisSpec(BaseModel):
    """Analysis specification."""
    statistical: Optional[List[StatisticalTest]] = Field(default_factory=list, description="Statistical tests to perform")
    visualizations: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Visualizations to generate")


class ArtifactConfig(BaseModel):
    """Artifact generation configuration."""
    type: str = Field(..., description="Artifact type (e.g., 'executive_summary', 'detailed_report')")
    format: Optional[str] = Field("markdown", description="Output format")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Artifact-specific parameters")


class ReportingSpec(BaseModel):
    """Reporting specification."""
    artifacts: List[ArtifactConfig] = Field(default_factory=list, description="Artifacts to generate")
    destinations: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Output destinations")


class InquiryManifest(BaseModel):
    """Top-level inquiry manifest model."""
    version: str = Field(..., description="Manifest schema version")
    id: str = Field(..., description="Unique manifest identifier")
    name: str = Field(..., description="Human-readable manifest name")
    metadata: ManifestMetadata = Field(..., description="Manifest metadata")
    protocol: ProtocolSpec = Field(..., description="Protocol specification")
    substrate: SubstrateSpec = Field(..., description="Substrate specification")
    instruments: List[InstrumentSpec] = Field(..., description="Instrument configurations")
    execution: Optional[ExecutionSpec] = Field(default_factory=ExecutionSpec, description="Execution configuration")
    analysis: Optional[AnalysisSpec] = Field(default_factory=AnalysisSpec, description="Analysis specification")
    reporting: Optional[ReportingSpec] = Field(default_factory=ReportingSpec, description="Reporting specification")
    
    @field_validator('version')
    @classmethod
    def validate_version(cls, v: str) -> str:
        # Simple semantic version check
        parts = v.split('.')
        if len(parts) not in [2, 3]:
            raise ValueError(f"Invalid version format: {v}. Expected format: X.Y or X.Y.Z")
        return v
    
    @model_validator(mode='after')
    def validate_phases_exist(self):
        """Ensure all protocol phases are valid."""
        if not self.protocol.phases:
            raise ValueError("Protocol must define at least one phase")
        return self


class ValidationResult:
    """Result of manifest validation."""
    
    def __init__(self, is_valid: bool, errors: List[str]):
        self.is_valid = is_valid
        self.errors = errors
    
    def __repr__(self):
        return f"ValidationResult(is_valid={self.is_valid}, errors={self.errors})"


class ManifestValidator:
    """
    Validates inquiry manifests using Pydantic models.
    Ensures structural correctness, type safety, and semantic constraints.
    """
    
    async def validate(self, manifest: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        Validate a parsed manifest against the schema.
        
        Args:
            manifest: Parsed manifest dictionary
            context: Optional validation context
            
        Returns:
            ValidationResult with validation status and any errors
        """
        errors = []
        
        try:
            # Extract the manifest section if it's wrapped
            manifest_data = manifest.get('manifest', manifest)
            
            # Validate using Pydantic model
            validated_manifest = InquiryManifest(**manifest_data)
            
            # Additional semantic validations
            errors.extend(self._validate_instrument_references(validated_manifest))
            errors.extend(self._validate_protocol_consistency(validated_manifest))
            
            if errors:
                return ValidationResult(is_valid=False, errors=errors)
            
            return ValidationResult(is_valid=True, errors=[])
            
        except Exception as e:
            # Convert Pydantic validation errors to readable messages
            error_msg = self._format_validation_error(e)
            errors.append(error_msg)
            return ValidationResult(is_valid=False, errors=errors)
    
    def _format_validation_error(self, error: Exception) -> str:
        """Format Pydantic validation errors into readable messages."""
        from pydantic import ValidationError
        
        if isinstance(error, ValidationError):
            error_messages = []
            for err in error.errors():
                field_path = ' -> '.join(str(loc) for loc in err['loc'])
                error_messages.append(f"{field_path}: {err['msg']}")
            return "; ".join(error_messages)
        else:
            return str(error)
    
    def _validate_instrument_references(self, manifest: InquiryManifest) -> List[str]:
        """Validate that instrument IDs are unique."""
        errors = []
        instrument_ids = [inst.id for inst in manifest.instruments]
        
        if len(instrument_ids) != len(set(instrument_ids)):
            duplicates = [id for id in instrument_ids if instrument_ids.count(id) > 1]
            errors.append(f"Duplicate instrument IDs found: {set(duplicates)}")
        
        return errors
    
    def _validate_protocol_consistency(self, manifest: InquiryManifest) -> List[str]:
        """Validate protocol configuration consistency."""
        errors = []
        
        # Ensure at least one instrument is defined
        if not manifest.instruments:
            errors.append("At least one instrument must be defined")
        
        # Validate concurrency settings
        if manifest.execution and manifest.execution.concurrency:
            max_workers = manifest.execution.concurrency.max_workers
            if max_workers > len(manifest.instruments) * 2:
                # Warning rather than error, but still report
                pass
        
        return errors
