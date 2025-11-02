"""Synthesis Agent performing multi-objective quantum optimization."""
from __future__ import annotations

import logging
from typing import Dict, List

from quantum.multi_objective_optimizer import MultiObjectiveOptimizer

logger = logging.getLogger(__name__)


class SynthesisAgent:
    """Combines scores from other agents into final recommendation weights."""

    def __init__(self) -> None:
        self.optimizer = MultiObjectiveOptimizer()

    def synthesize(self, candidate_scores: List[Dict[str, float]]) -> Dict[str, float]:
        if not candidate_scores:
            return {"overall": 0.0}
        aggregated = {}
        for score_bundle in candidate_scores:
            for key, value in score_bundle.items():
                aggregated.setdefault(key, 0.0)
                aggregated[key] += value
        weights = list(aggregated.values())
        scaling = self.optimizer.multi_objective(weights)
        logger.debug("Synthesis scaling factor: %s", scaling)
        return {k: round(v * scaling, 4) for k, v in aggregated.items()}
