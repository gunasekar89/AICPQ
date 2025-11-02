"""Minimal NumPy compatibility layer for environments without NumPy."""
from __future__ import annotations

import cmath
import math
import random
from typing import Iterable, List

try:  # pragma: no cover - optional dependency
    import numpy as np  # type: ignore
except Exception:  # noqa: BLE001
    class _NumpyCompat:
        @staticmethod
        def array(values: Iterable[float], dtype: type | None = None) -> List[float]:
            return [float(v) for v in values]

        @staticmethod
        def linalg_norm(vector: Iterable[float]) -> float:
            return math.sqrt(sum(float(v) ** 2 for v in vector))

        @staticmethod
        def zeros(length: int) -> List[float]:
            return [0.0] * length

        @staticmethod
        def fft(values: Iterable[float], n: int) -> List[complex]:
            values = list(values)
            if not values:
                return [0j] * n
            while len(values) < n:
                values.append(0.0)
            result = []
            for k in range(n):
                total = 0j
                for t, value in enumerate(values[:n]):
                    angle = -2j * math.pi * k * t / n
                    total += value * cmath.exp(angle)
                result.append(total)
            return result

        @staticmethod
        def random_rand(length: int) -> List[float]:
            return [random.random() for _ in range(length)]

        @staticmethod
        def exp(value: float) -> float:
            return math.exp(value)

        @staticmethod
        def var(values: Iterable[float]) -> float:
            values = list(values)
            if not values:
                return 0.0
            mean = sum(values) / len(values)
            return sum((v - mean) ** 2 for v in values) / len(values)

    class _CompatModule:
        def array(self, values: Iterable[float], dtype: type | None = None):
            return _NumpyCompat.array(values, dtype)

        def linalg_norm(self, vector: Iterable[float]) -> float:
            return _NumpyCompat.linalg_norm(vector)

        def zeros(self, length: int):
            return _NumpyCompat.zeros(length)

        def fft(self, values: Iterable[float], n: int):
            return _NumpyCompat.fft(values, n)

        def random_rand(self, length: int):
            return _NumpyCompat.random_rand(length)

        def exp(self, value: float):
            return _NumpyCompat.exp(value)

        def var(self, values: Iterable[float]):
            return _NumpyCompat.var(values)

    class _Linalg:
        @staticmethod
        def norm(vector: Iterable[float]) -> float:
            return _NumpyCompat.linalg_norm(vector)

    class _Random:
        @staticmethod
        def rand(length: int):
            return _NumpyCompat.random_rand(length)

    class _FFT:
        @staticmethod
        def fft(values: Iterable[float], n: int):
            return _NumpyCompat.fft(values, n)

    np = _CompatModule()  # type: ignore
    np.linalg = _Linalg()  # type: ignore[attr-defined]
    np.random = _Random()  # type: ignore[attr-defined]
    np.fft = _FFT()  # type: ignore[attr-defined]
else:  # pragma: no cover
    np = np

__all__ = ["np"]
