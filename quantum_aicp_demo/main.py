"""CLI entrypoint for the Quantum AICP Sneaker Recommendation Engine."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List

from agents.brand_agent import BrandAgent
from agents.fulfillment_agent import FulfillmentAgent
from agents.planner_agent import PlannerAgent
from agents.preference_agent import PreferenceAgent
from agents.quantum_agent import QuantumAgent
from agents.synthesis_agent import SynthesisAgent
from agents.vision_agent import VisionAgent
from config.settings import settings

logging.basicConfig(level=settings.logging.level, format=settings.logging.format)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_json(path: Path) -> List[Dict[str, any]]:
    with path.open("r") as f:
        return json.load(f)


def hybrid_pipeline(user_query: str, demo_user: str = "user_001") -> Dict[str, any]:
    logger.info("Starting hybrid quantum-classical pipeline")
    planner = PlannerAgent()
    quantum_agent = QuantumAgent()
    brand_agent = BrandAgent()
    vision_agent = VisionAgent(qcnn_qubits=settings.quantum.qcnn_qubits)
    preference_agent = PreferenceAgent(qubits=settings.quantum.qlstm_qubits)
    synthesis_agent = SynthesisAgent()
    fulfillment_agent = FulfillmentAgent()

    products = load_json(DATA_DIR / "demo_products.json")
    users = {u["user_id"]: u for u in load_json(DATA_DIR / "user_profiles.json")}
    user_profile = users.get(demo_user, next(iter(users.values())))

    intents = planner.parse_intent(user_query)
    logger.info("Planner intents: %s", intents)

    feature_map = {p["id"]: p["clip_features"][: settings.quantum.qcnn_qubits] for p in products[:6]}
    quantum_insights = quantum_agent.end_to_end_quantum_insight(feature_map)

    brand_rankings = brand_agent.rank_products(products[:10])
    preference_scores = preference_agent.preference_scores(user_profile)

    synthesis_scores = synthesis_agent.synthesize(
        [*({"eco": score} for _, score in brand_rankings[:5]), preference_scores]
    )

    orders = [
        {
            "order_id": f"order_{i}",
            "distance_km": 10 + i,
            "priority": 0.5 + i * 0.1,
            "eco_priority": 0.7,
        }
        for i in range(3)
    ]
    route_plan = fulfillment_agent.plan_routes(orders)

    return {
        "intents": intents,
        "quantum_insights": {pid: result.scores for pid, result in quantum_insights.items()},
        "brand_rankings": brand_rankings[:5],
        "preference_scores": preference_scores,
        "synthesis": synthesis_scores,
        "routes": route_plan,
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Quantum AICP Sneaker Recommendation Engine")
    parser.add_argument("query", nargs="?", default="Find the best sustainable sneakers for city running")
    parser.add_argument("--user", default="user_001")
    args = parser.parse_args()

    results = hybrid_pipeline(args.query, args.user)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
