"""Quantum Convolutional Neural Network operations for image features."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from .np_compat import np

logger = logging.getLogger(__name__)


@dataclass
class QCNNEngine:
    """Lightweight QCNN simulator for demo-friendly with mock data scenarios."""

    qubits: int = 4

    def apply(self, features: Iterable[float]):
        vector = np.array(list(features), dtype=float)
        if len(vector) == 0:
            return np.zeros(self.qubits)
        norm = np.linalg.norm(vector) or 1.0
        normalized = [v / norm for v in vector]
        enhanced = np.fft.fft(normalized, n=self.qubits)
        logger.debug("QCNN enhanced vector: %s", enhanced)
        return [float(getattr(val, "real", val)) for val in enhanced]
