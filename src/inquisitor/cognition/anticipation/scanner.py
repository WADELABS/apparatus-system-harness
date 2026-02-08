"""
Horizon Scanner
===============

The Anticipatory Intelligence Coordinator.
Integrates WeakSignalDetector and TrendConvergenceDetector to forecast future states.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

from .weak_signal import WeakSignalDetector, WeakSignal
from .trend_convergence import TrendConvergenceDetector, ConvergencePoint

logger = logging.getLogger(__name__)

@dataclass
class AnticipationEvent:
    """A forecasted future event or state."""
    description: str
    probability: float
    time_horizon: str # e.g., "near-term", "strategic"
    supporting_evidence: List[Any]
    created_at: datetime = datetime.now()

class HorizonScanner:
    """
    The main coordinator for anticipatory intelligence.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.weak_signal_detector = WeakSignalDetector(self.config.get('weak_signal'))
        self.trend_detector = TrendConvergenceDetector(self.config.get('trend'))
        
    async def scan_horizon(self, input_streams: Dict[str, List[Dict[str, Any]]]) -> List[AnticipationEvent]:
        """
        Perform a full horizon scan on provided input streams.
        """
        logger.info("Initiating Horizon Scan...")
        
        # 1. Flatten inputs for signal detection
        all_inputs = []
        for source, items in input_streams.items():
            for item in items:
                item['source'] = source
                all_inputs.append(item)
        
        # 2. Detect Weak Signals
        weak_signals = await self.weak_signal_detector.scan(all_inputs)
        logger.info(f"Detected {len(weak_signals)} weak signals.")
        
        # 3. Detect Convergences
        convergences = await self.trend_detector.analyze(weak_signals)
        logger.info(f"Identified {len(convergences)} trend convergences.")
        
        # 4. Synthesize Anticipation Events
        anticipations = []
        for conv in convergences:
            event = AnticipationEvent(
                description=f"Emergence of {conv.target_concept} driven by {conv.contributing_trends}",
                probability=conv.coherence_score,
                time_horizon="strategic",
                supporting_evidence=weak_signals # Ideally filter for relevant ones
            )
            anticipations.append(event)
            
        return anticipations

    async def run_daemon(self, stream_source):
        """
        Run in daemon mode, continuously scanning a stream.
        """
        while True:
            data = await stream_source.get()
            events = await self.scan_horizon({'stream': [data]})
            if events:
                # Dispatch events to some bus or log
                for evt in events:
                    logger.info(f"ANTICIPATION: {evt.description}")
            await asyncio.sleep(1)
