from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SPEC = importlib.util.spec_from_file_location("main", ROOT / "main.py")
main = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(main)


def test_hybrid_pipeline_runs():
    output = main.hybrid_pipeline("Eco sneakers for trail running", demo_user="user_001")
    assert "intents" in output
    assert "quantum_insights" in output
    assert len(output["brand_rankings"]) > 0
