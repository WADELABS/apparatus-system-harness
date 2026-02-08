import logging
import asyncio

logger = logging.getLogger(__name__)

class TelemetryCollector:
    def __init__(self, config=None):
        self.config = config or {}
        
    class Span:
        def __init__(self, name, logger):
            self.name = name
            self.logger = logger
            
        async def __aenter__(self):
            self.logger.debug(f"Starting span: {self.name}")
            return self
            
        async def __aexit__(self, exc_type, exc, tb):
            self.logger.debug(f"Ending span: {self.name}")
    
    def span(self, name, context):
        return self.Span(name, logger)

    async def record_phase_completion(self, name, context, result):
        logger.info(f"Phase completed: {name}")

    async def record_execution_failure(self, error, context):
        logger.error(f"Execution failure: {error}")

    async def record_instrument_ready(self, id):
        logger.info(f"Instrument ready: {id}")

    async def record_instrument_execution(self, id, result, context):
        logger.info(f"Instrument executed: {id}")

    async def record_instrument_failure(self, id, error, context):
        logger.error(f"Instrument failure {id}: {error}")

    async def record_instrument_error(self, id, type, error):
        logger.error(f"Instrument error {id} ({type}): {error}")

