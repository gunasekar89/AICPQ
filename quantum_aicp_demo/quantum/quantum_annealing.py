"""Quantum annealing approximations for delivery routing."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict

from config.settings import settings
from .np_compat import np

logger = logging.getLogger(__name__)


@dataclass
class AnnealingResult:
    scores: Dict[str, float]
    cost: float
    circuit: str
    mode: str


class QuantumAnnealer:
    """Simulates quantum annealing with Azure Quantum integration points."""

    def __init__(self) -> None:
        self.steps = settings.quantum.annealing_steps

    def solve(self, constraints: Dict[str, float]) -> AnnealingResult:
        vector = np.array(list(constraints.values()), dtype=float)
        anneal_path = [1.0 - (i / max(self.steps - 1, 1)) for i in range(self.steps)]
        noise = (np.random.rand(1)[0] - 0.5) * 0.02
        cost = float(sum(vector) * 0.5 + noise)
        circuit_repr = "\n".join(f"Step {i}: gamma={g:.3f}" for i, g in enumerate(anneal_path[:10]))
        denom = cost + 1e-6
        scores = {key: float(value / denom) for key, value in constraints.items()}
        logger.debug("Annealing result cost=%s scores=%s", cost, scores)
        return AnnealingResult(scores=scores, cost=cost, circuit=circuit_repr, mode="simulated")
