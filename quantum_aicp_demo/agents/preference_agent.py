"""Preference Agent using Quantum LSTM simulations for user pattern analysis."""
from __future__ import annotations

import logging
from typing import Dict, List

from quantum.multi_objective_optimizer import MultiObjectiveOptimizer
from quantum.np_compat import np

logger = logging.getLogger(__name__)


class PreferenceAgent:
    """Analyzes user histories with QLSTM inspired architecture."""

    def __init__(self, qubits: int = 6) -> None:
        self.qubits = qubits
        self.optimizer = MultiObjectiveOptimizer()

    def simulate_qlstm(self, user_sequence: List[float]) -> List[float]:
        sequence = np.array(user_sequence, dtype=float)
        if len(sequence) == 0:
            return [0.0] * self.qubits
        max_val = max(abs(v) for v in sequence) or 1.0
        weights = [__import__("math").tanh(v / max_val) for v in sequence]
        if len(weights) < self.qubits:
            weights.extend([0.0] * (self.qubits - len(weights)))
        return weights[: self.qubits]

    def preference_scores(self, user_profile: Dict[str, any]) -> Dict[str, float]:
        history = user_profile.get("purchase_history", [0.2, 0.5, 0.8])
        encoded = self.simulate_qlstm(history)
        score = self.optimizer.variational_score(encoded)
        return {"preference_score": float(score), "encoded": float(sum(encoded) / len(encoded))}
