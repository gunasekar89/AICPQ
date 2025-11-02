"""Planner Agent leveraging Gemini LLM for intent parsing."""
from __future__ import annotations

import json
import logging
import time
from typing import Dict, List

try:  # pragma: no cover - optional dependency
    import requests
except Exception:  # noqa: BLE001
    class _DummyRequests:
        class RequestException(Exception):
            pass

        class Session:
            headers: Dict[str, str] = {}

            def post(self, *_, **__):
                raise _DummyRequests.RequestException("requests not available")

    requests = _DummyRequests()  # type: ignore

from config.settings import settings

logger = logging.getLogger(__name__)


class PlannerAgent:
    """High level orchestrator translating natural language intents into agent plans."""

    def __init__(self) -> None:
        self.api_key = settings.gemini.api_key
        self.api_base = settings.gemini.api_base
        self.model = settings.gemini.model
        self.temperature = settings.gemini.temperature
        self.session = requests.Session()
        if hasattr(self.session, "headers"):
            self.session.headers.update({"Content-Type": "application/json"})
        if settings.logging.metrics_enabled:
            logger.info("PlannerAgent initialized with Gemini model %s", self.model)

    def parse_intent(self, user_input: str) -> Dict[str, List[str]]:
        """Call Gemini API to extract structured intents."""
        if not user_input.strip():
            logger.warning("Empty user input received; returning default intents")
            return {"tasks": ["collect_preferences", "compute_recommendations"]}

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": (
                                "You are the Planner Agent for a hybrid quantum-classical pipeline. "
                                "Parse the following request into a JSON object with keys tasks, "
                                "constraints, and context."
                            )
                        },
                        {"text": user_input},
                    ],
                }
            ],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": 512,
            },
        }

        url = f"{self.api_base}/models/{self.model}:generateContent"
        logger.debug("PlannerAgent calling Gemini endpoint %s", url)

        try:
            response = self.session.post(url, json=payload, params={"key": self.api_key}, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            logger.error("Gemini API error: %s", exc, exc_info=True)
            return {
                "tasks": ["collect_preferences", "compute_quantum_scores", "rank_products"],
                "constraints": ["fallback_mode"],
                "context": ["gemini_unavailable"],
            }

        parsed = self._coerce_to_dict(data)
        logger.debug("PlannerAgent parsed intents: %s", parsed)
        return parsed

    def _coerce_to_dict(self, data: Dict[str, any]) -> Dict[str, List[str]]:
        text = ""
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError):
            logger.warning("Unexpected Gemini response structure; returning defaults")
            return {
                "tasks": ["collect_preferences", "compute_quantum_scores", "rank_products"],
                "constraints": ["insufficient_response"],
                "context": ["fallback_parse"],
            }

        try:
            json_start = text.find("{")
            json_end = text.rfind("}")
            if json_start == -1 or json_end == -1:
                raise ValueError("No JSON found in Gemini response")
            json_str = text[json_start : json_end + 1]
            parsed = json.loads(json_str)
            return {
                "tasks": [str(t) for t in parsed.get("tasks", [])],
                "constraints": [str(c) for c in parsed.get("constraints", [])],
                "context": [str(c) for c in parsed.get("context", [])],
            }
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to parse Gemini response: %s", exc)
            return {
                "tasks": ["collect_preferences", "compute_quantum_scores", "rank_products"],
                "constraints": ["parse_failure"],
                "context": [text[:120]],
            }

    def healthcheck(self) -> Dict[str, str]:
        start = time.time()
        status = "ok"
        try:
            if not self.api_key:
                raise RuntimeError("Missing Gemini API key")
        except Exception as exc:  # noqa: BLE001
            logger.error("PlannerAgent healthcheck failed: %s", exc)
            status = "degraded"
        latency = time.time() - start
        return {"status": status, "latency": f"{latency:.4f}"}
