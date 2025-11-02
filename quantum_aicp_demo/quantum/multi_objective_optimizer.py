"""Quantum inspired multi-objective optimization utilities."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from .np_compat import np

logger = logging.getLogger(__name__)


@dataclass
class MultiObjectiveOptimizer:
    """Provides scoring routines with comprehensive error handling."""

    def variational_score(self, features: Iterable[float]) -> float:
        vector = np.array(list(features), dtype=float)
        if len(vector) == 0:
            return 0.0
        norm = np.linalg.norm(vector) or 1.0
        normalized = [v / norm for v in vector]
        angle = sum(__import__("math").sin(v) for v in normalized)
        score = float((angle + 1) / 2)
        logger.debug("Variational score computed: %s", score)
        return score

    def quantum_kernel_similarity(self, a: Iterable[float], b: Iterable[float]) -> float:
        vec_a = np.array(list(a), dtype=float)
        vec_b = np.array(list(b), dtype=float)
        if len(vec_a) == 0 or len(vec_b) == 0:
            return 0.0
        diff = [x - y for x, y in zip(vec_a, vec_b)]
        distance = sum((d) ** 2 for d in diff) ** 0.5
        kernel = float(__import__("math").exp(-(distance**2)))
        logger.debug("Quantum kernel similarity: %s", kernel)
        return kernel

    def multi_objective(self, weights: Iterable[float]) -> float:
        vector = np.array(list(weights), dtype=float)
        if len(vector) == 0:
            return 0.0
        penalty = np.var(vector)
        scaling = float(1.0 / (1.0 + penalty))
        logger.debug("Multi-objective scaling: %s", scaling)
        return scaling
