"""
ExecutionPlanCompiler: Compiles validated manifests into execution plans.
Builds DAG, handles phase dependencies, and generates execution steps.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ExecutionStep:
    """Individual execution step within a phase."""
    step_id: str
    phase: str
    instrument_id: str
    instrument_type: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    retry_policy: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    """Complete execution plan with phases, steps, and configuration."""
    phases: List[str]
    steps: List[ExecutionStep]
    concurrency_limit: int
    estimated_duration: int  # in seconds
    retry_policy: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionPlanCompiler:
    """
    Compiles validated manifests into executable plans.
    Generates execution DAG, handles dependencies, and calculates resource requirements.
    """
    
    async def compile(self, manifest: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> ExecutionPlan:
        """
        Compile a validated manifest into an execution plan.
        
        Args:
            manifest: Validated manifest (ParsedManifest or dict)
            context: Optional compilation context
            
        Returns:
            ExecutionPlan with phases, steps, and configuration
        """
        # Extract manifest data
        manifest_data = self._extract_manifest_data(manifest)
        
        # Extract protocol phases
        phases = self._extract_phases(manifest_data)
        
        # Build execution steps
        steps = self._build_execution_steps(manifest_data, phases)
        
        # Determine concurrency limit
        concurrency_limit = self._extract_concurrency_limit(manifest_data)
        
        # Extract retry policy
        retry_policy = self._extract_retry_policy(manifest_data)
        
        # Estimate execution duration
        estimated_duration = self._estimate_duration(manifest_data, steps)
        
        # Build metadata
        metadata = {
            'manifest_id': manifest_data.get('id', 'unknown'),
            'manifest_version': manifest_data.get('version', '1.0.0'),
            'protocol_type': manifest_data.get('protocol', {}).get('type', 'sequential'),
            'instrument_count': len(manifest_data.get('instruments', [])),
        }
        
        return ExecutionPlan(
            phases=phases,
            steps=steps,
            concurrency_limit=concurrency_limit,
            estimated_duration=estimated_duration,
            retry_policy=retry_policy,
            metadata=metadata
        )
    
    def _extract_manifest_data(self, manifest: Any) -> Dict[str, Any]:
        """Extract manifest data from various input formats."""
        if hasattr(manifest, 'data'):
            # ParsedManifest object
            data = manifest.data
        elif isinstance(manifest, dict):
            data = manifest
        else:
            raise ValueError(f"Unsupported manifest type: {type(manifest)}")
        
        # Handle wrapped manifest
        return data.get('manifest', data)
    
    def _extract_phases(self, manifest_data: Dict[str, Any]) -> List[str]:
        """Extract protocol phases from manifest."""
        protocol = manifest_data.get('protocol', {})
        
        # Handle both list and dict formats
        phases = protocol.get('phases', [])
        
        if not phases:
            # Default phases if not specified
            return ['initialization', 'execution', 'analysis']
        
        # Handle list of phase names
        if isinstance(phases, list):
            # Filter out dict entries if phases have detailed definitions
            phase_names = []
            for phase in phases:
                if isinstance(phase, str):
                    phase_names.append(phase)
                elif isinstance(phase, dict) and 'name' in phase:
                    phase_names.append(phase['name'])
            return phase_names if phase_names else phases
        
        return ['execution']  # Fallback
    
    def _build_execution_steps(self, manifest_data: Dict[str, Any], phases: List[str]) -> List[ExecutionStep]:
        """Build execution steps from manifest instruments and protocol."""
        steps = []
        instruments = manifest_data.get('instruments', [])
        protocol = manifest_data.get('protocol', {})
        execution_config = manifest_data.get('execution', {})
        
        # Extract retry policy
        retry_policy_config = execution_config.get('retry_policy', {})
        retry_policy = {
            'max_attempts': retry_policy_config.get('max_attempts', 1),
            'backoff_factor': retry_policy_config.get('backoff_factor', 1.0),
            'timeout': retry_policy_config.get('timeout')
        } if retry_policy_config else None
        
        # Check if protocol has detailed phase definitions
        protocol_phases = protocol.get('phases', [])
        has_detailed_phases = any(isinstance(p, dict) for p in protocol_phases) if protocol_phases else False
        
        if has_detailed_phases:
            # Build steps from detailed phase definitions
            for phase_def in protocol_phases:
                if isinstance(phase_def, dict):
                    phase_name = phase_def.get('name', 'unknown')
                    phase_steps = phase_def.get('steps', [])
                    
                    for idx, step_def in enumerate(phase_steps):
                        instrument_id = step_def.get('instrument', f'step_{idx}')
                        
                        step = ExecutionStep(
                            step_id=f"{phase_name}_{step_def.get('name', idx)}",
                            phase=phase_name,
                            instrument_id=instrument_id,
                            instrument_type=step_def.get('type', 'generic'),
                            parameters=step_def.get('parameters', {}),
                            retry_policy=retry_policy,
                            timeout=execution_config.get('timeout')
                        )
                        steps.append(step)
        else:
            # Build steps by distributing instruments across phases
            phase_count = len(phases)
            
            for idx, instrument in enumerate(instruments):
                # Distribute instruments across phases
                # Initialization phase: first 20% of instruments
                # Execution phase: middle 60% of instruments
                # Analysis phase: last 20% of instruments
                if phase_count >= 3:
                    if idx < len(instruments) * 0.2:
                        phase = phases[0]  # initialization
                    elif idx < len(instruments) * 0.8:
                        phase = phases[min(1, phase_count - 1)]  # execution
                    else:
                        phase = phases[min(2, phase_count - 1)]  # analysis
                else:
                    phase = phases[min(idx % phase_count, phase_count - 1)]
                
                step = ExecutionStep(
                    step_id=f"{phase}_{instrument.get('id', f'inst_{idx}')}",
                    phase=phase,
                    instrument_id=instrument.get('id', f'instrument_{idx}'),
                    instrument_type=instrument.get('type', 'unknown'),
                    parameters=instrument.get('parameters', {}),
                    retry_policy=retry_policy,
                    timeout=execution_config.get('timeout')
                )
                steps.append(step)
        
        return steps
    
    def _extract_concurrency_limit(self, manifest_data: Dict[str, Any]) -> int:
        """Extract concurrency limit from manifest."""
        execution = manifest_data.get('execution', {})
        concurrency = execution.get('concurrency', {})
        return concurrency.get('max_workers', 1)
    
    def _extract_retry_policy(self, manifest_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract retry policy from manifest."""
        execution = manifest_data.get('execution', {})
        retry_policy = execution.get('retry_policy', {})
        
        if retry_policy:
            return {
                'max_attempts': retry_policy.get('max_attempts', 1),
                'backoff_factor': retry_policy.get('backoff_factor', 1.0),
                'timeout': retry_policy.get('timeout')
            }
        return None
    
    def _estimate_duration(self, manifest_data: Dict[str, Any], steps: List[ExecutionStep]) -> int:
        """
        Estimate execution duration based on steps and concurrency.
        Returns estimated duration in seconds.
        """
        if not steps:
            return 0
        
        # Base time per step (estimated at 30 seconds per instrument)
        base_time_per_step = 30
        
        # Get concurrency limit
        concurrency_limit = self._extract_concurrency_limit(manifest_data)
        
        # Group steps by phase to account for sequential phase execution
        phases = {}
        for step in steps:
            if step.phase not in phases:
                phases[step.phase] = []
            phases[step.phase].append(step)
        
        # Calculate duration: phases run sequentially, steps within phases run in parallel
        total_duration = 0
        for phase_steps in phases.values():
            # With concurrency, time = (steps / workers) * base_time
            phase_duration = (len(phase_steps) / concurrency_limit) * base_time_per_step
            total_duration += int(phase_duration)
        
        return total_duration
