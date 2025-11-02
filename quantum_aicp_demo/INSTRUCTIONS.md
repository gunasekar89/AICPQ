# Quantum AICP Sneaker Recommendation Engine — Setup Reference

This repository keeps the authoritative setup guide at the project root in [`../INSTRUCTIONS.md`](../INSTRUCTIONS.md).

If you cloned only the `quantum_aicp_demo` package directory or are browsing an install artifact that excludes top-level docs,
use the linked guide above for the complete "production-ready code" walkthrough, including demo-friendly configuration, Azure Quantum integration points, and hybrid quantum-classical pipeline instructions.

A quick summary of the most common local commands:

```bash
# set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run the Streamlit dashboard
streamlit run frontend/streamlit_app.py

# execute the demo pipeline test
pytest tests/test_pipeline.py -q
```

For Docker usage, environment variables, and troubleshooting tips, consult the full guide in `../INSTRUCTIONS.md`.
