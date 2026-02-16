"""
Echo Instrument
===============

A basic instrument that echoes input parameters. Used for testing and calibration.
"""

from typing import Dict, Any
import asyncio
from ..base.instrument import AbstractInstrument, InstrumentConfig

class EchoInstrument(AbstractInstrument):
    """
    Basic instrument that echoes inputs.
    """
    
    def _parse_parameters(self, raw_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters."""
        return raw_parameters
    
    async def _perform_initialization(self):
        """No initialization needed."""
        pass
    
    async def _collect_calibration_data(self) -> Dict[str, Any]:
        """No calibration data needed."""
        return {}
    
    async def _perform_calibration(self, data: Dict[str, Any]):
        """No calibration needed."""
        from ..base.instrument import CalibrationResult
        return CalibrationResult(success=True, metrics={}, artifacts={})

    def _validate_calibration(self, result) -> bool:
        return True

    async def _validate_execution_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        return parameters
    
    async def _perform_execution(self, parameters: Dict[str, Any],
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """Echo the parameters after a delay."""
        delay = self.config.parameters.get('response_delay_ms', 0) / 1000.0
        if delay > 0:
            await asyncio.sleep(delay)
            
        return {
            'echo': parameters,
            'timestamp': str(context.get('start_time'))
        }
