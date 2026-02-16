"""
Abstract base class for all instruments.
Implements calibration, diagnostics, and execution lifecycle.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Type, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime
from pathlib import Path
import json
import pickle
from contextlib import asynccontextmanager
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from pydantic import BaseModel, Field, validator
import numpy as np

# Placeholder imports
from typing import Protocol, runtime_checkable

@runtime_checkable
class TelemetryCollector(Protocol):
    def span(self, name, context) -> Any: ...
    async def record_instrument_ready(self, id: str): ...
    async def record_instrument_error(self, id: str, type: str, error: Exception): ...
    async def record_instrument_execution(self, id: str, result: Any, context: Dict[str, Any]): ...
    async def record_instrument_failure(self, id: str, error: Exception, context: Dict[str, Any]): ...
    async def record_checkpoint_created(self, id: str, path: str, meta: Dict[str, Any]): ...
    async def record_checkpoint_restored(self, id: str, path: str): ...

@runtime_checkable
class ProvenanceRecorder(Protocol):
    async def record_calibration(self, id: str, result: Any, config: Any): ...
    async def record_execution(self, instrument_id: str, result: Any, context: Dict[str, Any]): ...
    async def record_execution_failure(self, instrument_id: str, error: Exception, result: Any, context: Dict[str, Any]): ...


class InstrumentCapability(Enum):
    """Capabilities that instruments can declare."""
    STATELESS = "stateless"           # No internal state between executions
    STATEFUL = "stateful"             # Maintains state across executions
    CALIBRATABLE = "calibratable"     # Can be calibrated
    MONITORABLE = "monitorable"       # Supports runtime monitoring
    DISTRIBUTABLE = "distributable"   # Can be distributed across nodes
    CHECKPOINTABLE = "checkpointable" # Can save/restore state


class InstrumentState(Enum):
    """Instrument lifecycle states."""
    UNINITIALIZED = "uninitialized"
    CALIBRATING = "calibrating"
    READY = "ready"
    EXECUTING = "executing"
    ERROR = "error"
    DEGRADED = "degraded"


@dataclass
class CalibrationResult:
    """Result of instrument calibration."""
    success: bool
    metrics: Dict[str, float]
    artifacts: Dict[str, Any]
    calibration_data: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)


class InstrumentConfig(BaseModel):
    """Configuration model for instrument initialization."""
    id: str
    type: str
    version: str = "1.0.0"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    calibration: Optional[Dict[str, Any]] = None
    capabilities: List[InstrumentCapability] = Field(default_factory=list)
    requirements: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True
    
    @validator('capabilities')
    def validate_capabilities(cls, v):
        # Ensure unique capabilities
        return list(set(v))


class ExecutionResult(BaseModel):
    """Standardized result from instrument execution."""
    success: bool
    data: Dict[str, Any]
    metrics: Dict[str, float] = Field(default_factory=dict)
    artifacts: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
    execution_time: float
    timestamp: datetime = Field(default_factory=datetime.now)
    
    @validator('metrics')
    def validate_metrics(cls, v):
        # Ensure all metric values are numeric
        for key, value in v.items():
            if not isinstance(value, (int, float, np.number)):
                raise ValueError(f"Metric '{key}' must be numeric")
        return v


class AbstractInstrument(ABC):
    """
    Abstract base class for all instruments.
    Implements comprehensive lifecycle management, calibration, and diagnostics.
    """
    
    # Class-level registry
    _registry: Dict[str, Type['AbstractInstrument']] = {}
    
    def __init_subclass__(cls, **kwargs):
        """Auto-register instrument subclasses."""
        super().__init_subclass__(**kwargs)
        instrument_type = getattr(cls, 'INSTRUMENT_TYPE', cls.__name__)
        cls._registry[instrument_type] = cls
    
    def __init__(self, config: InstrumentConfig, telemetry: TelemetryCollector, provenance: Optional['ProvenanceRecorder'] = None):
        self.config = config
        self.telemetry = telemetry
        self.provenance = provenance
        
        # State management
        self._state: InstrumentState = InstrumentState.UNINITIALIZED
        self._state_lock = asyncio.Lock()
        
        # Calibration data
        self._calibration_data: Optional[Dict[str, Any]] = None
        self._calibration_result: Optional[CalibrationResult] = None
        
        # Execution history
        self._execution_history: List[ExecutionResult] = []
        self._error_history: List[Dict[str, Any]] = []
        
        # Performance metrics
        self._performance_stats: Dict[str, List[float]] = {
            'execution_times': [],
            'success_rate': []
        }
        
        # Initialize with configuration
        self._initialize_from_config(config)
    
    def _initialize_from_config(self, config: InstrumentConfig):
        """Initialize instrument from configuration."""
        self.id = config.id
        self.type = config.type
        self.version = config.version
        self.capabilities = set(config.capabilities)
        self.requirements = config.requirements
        
        # Parse and validate parameters
        self.parameters = self._parse_parameters(config.parameters)
        
        # Set up calibration if specified
        if config.calibration:
            self._setup_calibration(config.calibration)
    
    @abstractmethod
    def _parse_parameters(self, raw_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate instrument-specific parameters."""
        pass
    
    def _setup_calibration(self, calibration_config: Dict[str, Any]):
        """Set up calibration procedure."""
        self.calibration_config = calibration_config
        self.calibration_required = calibration_config.get('required', False)
        self.calibration_interval = calibration_config.get('interval_seconds', 3600)
        self._last_calibration: Optional[datetime] = None
    
    async def initialize(self) -> bool:
        """Initialize instrument and perform any required setup."""
        async with self._state_lock:
            if self._state != InstrumentState.UNINITIALIZED:
                raise InstrumentStateError(
                    f"Cannot initialize from state {self._state}"
                )
            
            try:
                # Perform instrument-specific initialization
                await self._perform_initialization()
                
                # Calibrate if required
                if getattr(self, 'calibration_required', False):
                    await self.calibrate(force=True)
                elif hasattr(self, 'calibration_config'):
                    # Optional calibration
                    await self.calibrate(force=False)
                
                self._state = InstrumentState.READY
                await self.telemetry.record_instrument_ready(self.id)
                
                return True
                
            except Exception as e:
                self._state = InstrumentState.ERROR
                await self._record_error("initialization_failed", e)
                raise InstrumentInitializationError(
                    f"Instrument {self.id} initialization failed: {str(e)}"
                )
    
    @abstractmethod
    async def _perform_initialization(self):
        """Instrument-specific initialization."""
        pass
    
    async def calibrate(self, force: bool = False) -> CalibrationResult:
        """Calibrate the instrument."""
        if InstrumentCapability.CALIBRATABLE not in self.capabilities:
            return CalibrationResult(
                success=True,
                metrics={},
                artifacts={},
                calibration_data=None
            )
        
        # Check if calibration is needed
        if not force and not self._calibration_needed():
            return self._calibration_result
        
        async with self._state_lock:
            self._state = InstrumentState.CALIBRATING
            
            try:
                calibration_data = await self._collect_calibration_data()
                
                # Perform calibration
                result = await self._perform_calibration(calibration_data)
                
                # Validate calibration
                if not self._validate_calibration(result):
                    raise CalibrationError("Calibration validation failed")
                
                # Update state
                self._calibration_data = calibration_data
                self._calibration_result = result
                self._last_calibration = datetime.now()
                self._state = InstrumentState.READY
                
                # Record calibration
                await self.provenance.record_calibration(
                    self.id, result, self.config
                )
                
                return result
                
            except Exception as e:
                self._state = InstrumentState.ERROR
                await self._record_error("calibration_failed", e)
                raise CalibrationError(f"Calibration failed: {str(e)}")
    
    def _calibration_needed(self) -> bool:
        """Check if calibration is needed."""
        if not self._last_calibration:
            return True
        
        if not hasattr(self, 'calibration_interval'):
            return False
        
        elapsed = (datetime.now() - self._last_calibration).total_seconds()
        return elapsed > self.calibration_interval
    
    @abstractmethod
    async def _collect_calibration_data(self) -> Dict[str, Any]:
        """Collect data needed for calibration."""
        pass
    
    @abstractmethod
    async def _perform_calibration(self, data: Dict[str, Any]) -> CalibrationResult:
        """Perform the calibration procedure."""
        pass
    
    @abstractmethod
    def _validate_calibration(self, result: CalibrationResult) -> bool:
        """Validate calibration result."""
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)) # Broad exception for now
    )
    async def execute(self, parameters: Dict[str, Any], 
                     context: Dict[str, Any]) -> ExecutionResult:
        """
        Execute the instrument with given parameters and context.
        Implements retry logic and comprehensive monitoring.
        """
        execution_id = context.get('execution_id', 'unknown')
        start_time = datetime.now()
        
        # Check if instrument is ready
        if self._state != InstrumentState.READY:
            raise InstrumentNotReadyError(
                f"Instrument {self.id} is not ready (state: {self._state})"
            )
        
        # Validate parameters
        validated_params = await self._validate_execution_parameters(parameters)
        
        # Create execution context
        execution_context = {
            **context,
            'instrument_id': self.id,
            'instrument_version': self.version,
            'parameters': validated_params,
            'start_time': start_time
        }
        
        # Start telemetry span
        async with self.telemetry.span(f"instrument_execution:{self.id}", 
                                      execution_context):
            
            try:
                # Update state
                async with self._state_lock:
                    self._state = InstrumentState.EXECUTING
                
                # Perform pre-execution checks
                await self._pre_execution_checks(validated_params, execution_context)
                
                # Execute instrument-specific logic
                result_data = await self._perform_execution(
                    validated_params, execution_context
                )
                
                # Post-process results
                processed_data = await self._post_process_results(
                    result_data, execution_context
                )
                
                # Calculate metrics
                execution_time = (datetime.now() - start_time).total_seconds()
                metrics = await self._calculate_execution_metrics(
                    processed_data, execution_time, execution_context
                )
                
                # Create execution result
                result = ExecutionResult(
                    success=True,
                    data=processed_data,
                    metrics=metrics,
                    execution_time=execution_time
                )
                
                # Update performance statistics
                self._update_performance_stats(result)
                
                # Record execution
                await self._record_execution(result, execution_context)
                
                return result
                
            except Exception as e:
                # Handle execution failure
                execution_time = (datetime.now() - start_time).total_seconds()
                
                error_result = ExecutionResult(
                    success=False,
                    data={},
                    metrics={'execution_time': execution_time},
                    errors=[str(e)],
                    execution_time=execution_time
                )
                
                await self._record_execution_failure(error_result, e, execution_context)
                
                # Update state based on error type
                if isinstance(e, TransientError):
                    self._state = InstrumentState.READY
                else:
                    self._state = InstrumentState.ERROR
                
                raise
                
            finally:
                # Ensure state is reset if still in EXECUTING state
                if self._state == InstrumentState.EXECUTING:
                    self._state = InstrumentState.READY
    
    @abstractmethod
    async def _validate_execution_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize execution parameters."""
        pass
    
    async def _pre_execution_checks(self, parameters: Dict[str, Any],
                                   context: Dict[str, Any]):
        """Perform pre-execution checks."""
        # Check resource requirements
        if 'resource_requirements' in self.requirements:
            # TODO: Implement actual resource availability check with Scheduler
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Resource requirements check not implemented for {self.id}: {self.requirements['resource_requirements']}")
        
        # Check calibration status
        if getattr(self, 'calibration_required', False) and not self._calibration_result:
            raise CalibrationRequiredError("Instrument requires calibration")
    
    @abstractmethod
    async def _perform_execution(self, parameters: Dict[str, Any],
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """Instrument-specific execution logic."""
        pass
    
    async def _post_process_results(self, raw_data: Dict[str, Any],
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process raw execution results."""
        # Apply calibration corrections if available
        if self._calibration_data:
            calibrated_data = await self._apply_calibration_corrections(
                raw_data, self._calibration_data
            )
        else:
            calibrated_data = raw_data
        
        # Apply any instrument-specific post-processing
        processed_data = await self._instrument_specific_post_processing(
            calibrated_data, context
        )
        
        return processed_data
    
    async def _apply_calibration_corrections(self, data: Dict[str, Any],
                                           calibration_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply calibration corrections to data."""
        return data
    
    async def _instrument_specific_post_processing(self, data: Dict[str, Any],
                                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """Instrument-specific post-processing."""
        return data
    
    async def _calculate_execution_metrics(self, data: Dict[str, Any],
                                          execution_time: float,
                                          context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate execution metrics."""
        metrics = {
            'execution_time_seconds': execution_time,
            'data_size': len(str(data))
        }
        
        # Add instrument-specific metrics
        instrument_metrics = await self._calculate_instrument_specific_metrics(
            data, context
        )
        metrics.update(instrument_metrics)
        
        return metrics
    
    async def _calculate_instrument_specific_metrics(self, data: Dict[str, Any],
                                                   context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate instrument-specific metrics."""
        return {}
    
    def _update_performance_stats(self, result: ExecutionResult):
        """Update performance statistics."""
        self._execution_history.append(result)
        self._performance_stats['execution_times'].append(result.execution_time)
        self._performance_stats['success_rate'].append(1.0 if result.success else 0.0)
        
        # Keep only recent history
        max_history = 1000
        if len(self._execution_history) > max_history:
            self._execution_history = self._execution_history[-max_history:]
            self._performance_stats['execution_times'] = self._performance_stats['execution_times'][-max_history:]
            self._performance_stats['success_rate'] = self._performance_stats['success_rate'][-max_history:]
    
    async def _record_execution(self, result: ExecutionResult,
                               context: Dict[str, Any]):
        """Record successful execution."""
        await self.provenance.record_execution(
            instrument_id=self.id,
            result=result,
            context=context
        )
        
        await self.telemetry.record_instrument_execution(
            self.id, result, context
        )
    
    async def _record_execution_failure(self, result: ExecutionResult,
                                       error: Exception,
                                       context: Dict[str, Any]):
        """Record execution failure."""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'instrument_id': self.id,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'result': result.dict()
        }
        
        self._error_history.append(error_record)
        
        await self.provenance.record_execution_failure(
            instrument_id=self.id,
            error=error,
            result=result,
            context=context
        )
        
        await self.telemetry.record_instrument_failure(
            self.id, error, context
        )
    
    async def _record_error(self, error_type: str, error: Exception):
        """Record general instrument error."""
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'instrument_id': self.id,
            'error_type': error_type,
            'error_message': str(error),
            'instrument_state': self._state.value
        }
        
        self._error_history.append(error_record)
        await self.telemetry.record_instrument_error(self.id, error_type, error)


# Custom exceptions for instrument errors
class InstrumentError(Exception):
    pass

class InstrumentStateError(InstrumentError):
    pass

class InstrumentInitializationError(InstrumentError):
    pass

class CalibrationError(InstrumentError):
    pass

class CalibrationRequiredError(InstrumentError):
    pass

class InstrumentNotReadyError(InstrumentError):
    pass

class TransientError(InstrumentError):
    pass

class CheckpointNotSupportedError(InstrumentError):
    pass

class CheckpointError(InstrumentError):
    pass

class CheckpointValidationError(CheckpointError):
    pass

class RestoreError(InstrumentError):
    pass
