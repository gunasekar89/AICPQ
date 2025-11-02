"""Quantum Optimization & Insight Agent with Azure Quantum integration points."""
from __future__ import annotations

import json
import logging
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from config.settings import settings
from quantum.multi_objective_optimizer import MultiObjectiveOptimizer
from quantum.qcnn_operations import QCNNEngine
from quantum.quantum_annealing import QuantumAnnealer

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    import qsharp
    from azure.quantum import Workspace
    from azure.quantum.optimization import Problem
except Exception:  # noqa: BLE001
    qsharp = None
    Workspace = None
    Problem = None

try:  # pragma: no cover - optional dependency
    from qiskit import Aer, QuantumCircuit
    from qiskit.utils import QuantumInstance
except Exception:  # noqa: BLE001
    Aer = None
    QuantumCircuit = None
    QuantumInstance = None


@dataclass
class QuantumResult:
    scores: Dict[str, float]
    metadata: Dict[str, str]
    circuit_visualization: str


class QuantumAgent:
    """Handles all quantum workloads in a hybrid quantum-classical pipeline."""

    def __init__(self) -> None:
        self.settings = settings
        self.annealer = QuantumAnnealer()
        self.optimizer = MultiObjectiveOptimizer()
        self.qcnn = QCNNEngine(qubits=settings.quantum.qcnn_qubits)
        self.workspace = self._init_workspace()
        logger.info("QuantumAgent initialized. Azure workspace configured: %s", bool(self.workspace))

    def _init_workspace(self) -> Optional["Workspace"]:
        if Workspace is None:
            logger.warning("Azure Quantum SDK not available; using local simulation mode")
            return None
        try:
            workspace = Workspace(**self.settings.azure.as_dict())
            logger.info("Connected to Azure Quantum workspace %s", workspace.workspace_name)
            return workspace
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to connect to Azure Quantum workspace: %s", exc)
            return None

    def run_constraint_optimization(self, constraints: Dict[str, float]) -> QuantumResult:
        logger.debug("Running quantum annealing with constraints %s", constraints)
        annealing_output = self.annealer.solve(constraints)
        metadata = {"mode": annealing_output.mode}
        if self.workspace and Problem is not None:
            metadata["provider"] = "azure_quantum"
        else:
            metadata["provider"] = "local_simulator"
        return QuantumResult(scores=annealing_output.scores, metadata=metadata, circuit_visualization=annealing_output.circuit)

    def run_variational_scoring(self, features: List[float]) -> QuantumResult:
        logger.debug("Running VQC scoring for features %s", features)
        visualization = ""
        if qsharp:
            visualization = self._render_qsharp_vqc(len(features))
        score = self.optimizer.variational_score(features)
        return QuantumResult(scores={"variational": score}, metadata={"provider": "qsharp" if qsharp else "local"}, circuit_visualization=visualization)

    def run_kernel_similarity(self, feature_a: List[float], feature_b: List[float]) -> QuantumResult:
        logger.debug("Running quantum kernel similarity")
        kernel_value = self.optimizer.quantum_kernel_similarity(feature_a, feature_b)
        circ_vis = self._build_kernel_circuit(len(feature_a))
        return QuantumResult(
            scores={"kernel_similarity": kernel_value},
            metadata={"provider": "qiskit" if QuantumCircuit else "approximate"},
            circuit_visualization=circ_vis,
        )

    def _render_qsharp_vqc(self, feature_dim: int) -> str:
        if not qsharp:
            return "Q# not available"
        try:
            qsharp.compile("operation DemoVQCCircuit() : Unit { body { Message(\"VQC Demo\"); } }")
            return "Q# VQC Circuit compiled"
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to compile Q# VQC: %s", exc)
            return "Q# compilation failed"

    def _build_kernel_circuit(self, feature_dim: int) -> str:
        if QuantumCircuit is None or Aer is None:
            return "Kernel circuit approximated"
        circuit = QuantumCircuit(feature_dim)
        for i in range(feature_dim):
            circuit.h(i)
        for i in range(feature_dim - 1):
            circuit.cx(i, i + 1)
        backend = Aer.get_backend("statevector_simulator")
        instance = QuantumInstance(backend)
        result = instance.execute(circuit)
        return circuit.draw(output="text") + f"\nStatevector length: {len(result.get_statevector())}"

    def end_to_end_quantum_insight(self, product_features: Dict[str, List[float]]) -> Dict[str, QuantumResult]:
        insight: Dict[str, QuantumResult] = {}
        for product_id, features in product_features.items():
            constraint_result = self.run_constraint_optimization({"budget": random.uniform(0.3, 0.9)})
            variational_result = self.run_variational_scoring(features)
            insight[product_id] = QuantumResult(
                scores={
                    **constraint_result.scores,
                    **variational_result.scores,
                },
                metadata={**constraint_result.metadata, "variational_provider": variational_result.metadata["provider"]},
                circuit_visualization=variational_result.circuit_visualization or constraint_result.circuit_visualization,
            )
        return insight

    def healthcheck(self) -> Dict[str, str]:
        return {
            "workspace": "connected" if self.workspace else "simulator",
            "qsharp": "available" if qsharp else "missing",
            "qiskit": "available" if QuantumCircuit else "missing",
        }
