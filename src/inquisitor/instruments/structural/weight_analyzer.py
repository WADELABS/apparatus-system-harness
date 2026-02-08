from ..base.instrument import AbstractInstrument

class WeightAnalyzer(AbstractInstrument):
    async def _parse_parameters(self, raw): return raw
    async def _perform_initialization(self): pass
    async def _collect_calibration_data(self): return {}
    async def _perform_calibration(self, data): return None
    async def _validate_calibration(self, result): return True
    async def _validate_execution_parameters(self, params): return params
    async def _perform_execution(self, params, context): return {"weights": []}
