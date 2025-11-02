"""Brand Agent responsible for eco-scoring with quantum-enhanced ranking."""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from quantum.multi_objective_optimizer import MultiObjectiveOptimizer

logger = logging.getLogger(__name__)


class BrandAgent:
    """Calculates sustainability metrics and ranks brands using hybrid techniques."""

    def __init__(self) -> None:
        self.optimizer = MultiObjectiveOptimizer()

    def eco_score(self, product: Dict[str, any]) -> float:
        components = [
            float(product.get("sustainability_score", 0.0)),
            float(product.get("recycled_material", 0.0)),
            float(product.get("carbon_offset", 0.0)),
        ]
        score = sum(components) / max(len(components), 1)
        logger.debug("Base eco score for %s: %s", product.get("name", "unknown"), score)
        return score

    def rank_products(self, products: List[Dict[str, any]]) -> List[Tuple[str, float]]:
        if not products:
            return []
        sustainability_vector = [self.eco_score(p) for p in products]
        quantum_boost = self.optimizer.variational_score(sustainability_vector)
        logger.debug("Quantum boost applied to eco scores: %s", quantum_boost)
        rankings = []
        for product, base_score in zip(products, sustainability_vector):
            adjusted = base_score * (1.0 + quantum_boost)
            rankings.append((product.get("name", "unknown"), round(adjusted, 3)))
        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings
