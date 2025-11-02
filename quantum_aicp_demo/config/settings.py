"""Configuration settings for the Quantum AICP Sneaker Recommendation Engine.

This module provides environment-aware configuration for demo-friendly with mock data,
production-ready code that integrates Azure Quantum integration points and Gemini API
credentials. The configuration is modular and extensible so that future enhancements can
reuse the same settings container.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict


def _bool_env(var_name: str, default: bool = False) -> bool:
    value = os.getenv(var_name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AzureQuantumSettings:
    """Settings required to connect to Azure Quantum workspace."""

    subscription_id: str = os.getenv("AZURE_QUANTUM_SUBSCRIPTION_ID", "demo-subscription")
    resource_group: str = os.getenv("AZURE_QUANTUM_RESOURCE_GROUP", "demo-resource-group")
    workspace_name: str = os.getenv("AZURE_QUANTUM_WORKSPACE", "demo-workspace")
    location: str = os.getenv("AZURE_QUANTUM_LOCATION", "westus")
    storage_account: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")

    def as_dict(self) -> Dict[str, str]:
        return {
            "subscription_id": self.subscription_id,
            "resource_group": self.resource_group,
            "workspace_name": self.workspace_name,
            "location": self.location,
            "storage_account": self.storage_account,
        }


@dataclass(frozen=True)
class GeminiSettings:
    """Settings for Gemini LLM gateway."""

    api_key: str = os.getenv("GEMINI_API_KEY", "demo-gemini-key")
    api_base: str = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta")
    model: str = os.getenv("GEMINI_MODEL", "models/gemini-pro")
    temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))


@dataclass(frozen=True)
class DatabaseSettings:
    """SQLite demo database configuration."""

    db_path: Path = Path(os.getenv("AICP_DB_PATH", "quantum_aicp_demo/data/demo.db"))
    echo: bool = _bool_env("AICP_DB_ECHO", False)


@dataclass(frozen=True)
class QuantumModelParameters:
    """Model parameters for quantum circuits."""

    qcnn_qubits: int = int(os.getenv("AICP_QCNN_QUBITS", "4"))
    qcnn_layers: int = int(os.getenv("AICP_QCNN_LAYERS", "3"))
    qlstm_qubits: int = int(os.getenv("AICP_QLSTM_QUBITS", "6"))
    annealing_steps: int = int(os.getenv("AICP_Q_ANNEALING_STEPS", "100"))
    vqe_layers: int = int(os.getenv("AICP_VQE_LAYERS", "4"))
    kernel_shots: int = int(os.getenv("AICP_KERNEL_SHOTS", "2048"))


@dataclass(frozen=True)
class LoggingSettings:
    """Logging configuration for the application."""

    level: int = getattr(logging, os.getenv("AICP_LOG_LEVEL", "INFO").upper(), logging.INFO)
    format: str = os.getenv(
        "AICP_LOG_FORMAT",
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )
    metrics_enabled: bool = _bool_env("AICP_LOG_METRICS", True)


@dataclass(frozen=True)
class DemoSettings:
    """Toggle demo mode and canned scenarios."""

    demo_mode: bool = _bool_env("AICP_DEMO_MODE", True)
    preload_scenarios: bool = _bool_env("AICP_PRELOAD_SCENARIOS", True)


@dataclass(frozen=True)
class APISettings:
    """RESTful API rate limiting and caching."""

    rate_limit_per_minute: int = int(os.getenv("AICP_API_RATE_LIMIT", "60"))
    cache_ttl_seconds: int = int(os.getenv("AICP_CACHE_TTL", "300"))


@dataclass(frozen=True)
class Settings:
    """Unified settings container."""

    azure: AzureQuantumSettings = field(default_factory=AzureQuantumSettings)
    gemini: GeminiSettings = field(default_factory=GeminiSettings)
    database: DatabaseSettings = field(default_factory=DatabaseSettings)
    quantum: QuantumModelParameters = field(default_factory=QuantumModelParameters)
    logging: LoggingSettings = field(default_factory=LoggingSettings)
    demo: DemoSettings = field(default_factory=DemoSettings)
    api: APISettings = field(default_factory=APISettings)

    @classmethod
    def load(cls) -> "Settings":
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "azure": self.azure.as_dict(),
            "gemini": {
                "api_key": "***redacted***" if self.gemini.api_key else "",
                "api_base": self.gemini.api_base,
                "model": self.gemini.model,
                "temperature": self.gemini.temperature,
            },
            "database": {
                "db_path": str(self.database.db_path),
                "echo": self.database.echo,
            },
            "quantum": {
                "qcnn_qubits": self.quantum.qcnn_qubits,
                "qcnn_layers": self.quantum.qcnn_layers,
                "qlstm_qubits": self.quantum.qlstm_qubits,
                "annealing_steps": self.quantum.annealing_steps,
                "vqe_layers": self.quantum.vqe_layers,
                "kernel_shots": self.quantum.kernel_shots,
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "metrics_enabled": self.logging.metrics_enabled,
            },
            "demo": {
                "demo_mode": self.demo.demo_mode,
                "preload_scenarios": self.demo.preload_scenarios,
            },
            "api": {
                "rate_limit_per_minute": self.api.rate_limit_per_minute,
                "cache_ttl_seconds": self.api.cache_ttl_seconds,
            },
        }


settings = Settings.load()
