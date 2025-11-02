# Quantum AICP Sneaker Recommendation Engine — Local Setup Guide

This document explains how to run the **Quantum AICP Sneaker Recommendation Engine** demo locally. The project ships with production-ready code patterns that remain demo-friendly with mock data, so you can explore the hybrid quantum-classical pipeline without external services.

## 1. Prerequisites

- Python 3.10 or newer (3.8+ supported, 3.10 recommended)
- Git
- Optional: Docker (for containerized runs)
- Optional: Access credentials for Azure Quantum and Gemini API if you want to connect to live services

## 2. Clone the repository

```bash
git clone <repository-url>
cd AICPQ
```

## 3. Python virtual environment

Using `venv` (replace with `conda` or other tools if preferred):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

Install the core and optional Azure Quantum dependencies in one step:

```bash
pip install --upgrade pip
pip install -r quantum_aicp_demo/requirements.txt
```

> **Note:** The `qsharp` and `azure-quantum` packages are large. If you only want to explore the demo mode with local simulators, you can omit them by editing `requirements.txt` before installing.

## 5. Environment variables (optional but recommended)

Create a `.env` file or export variables in your shell before running the app. The following variables override the defaults defined in `quantum_aicp_demo/config/settings.py`:

```bash
export GEMINI_API_KEY="your-gemini-key"
export GEMINI_API_BASE="https://generativelanguage.googleapis.com/v1beta"
export GEMINI_MODEL="models/gemini-pro"

export AZURE_QUANTUM_SUBSCRIPTION_ID="00000000-0000-0000-0000-000000000000"
export AZURE_QUANTUM_RESOURCE_GROUP="your-resource-group"
export AZURE_QUANTUM_WORKSPACE="your-workspace"
export AZURE_QUANTUM_LOCATION="westus"

export AICP_DEMO_MODE=true   # keep true to use bundled mock data
```

If the Azure or Gemini credentials are not supplied, the system automatically falls back to local simulators and offline planners so you can still run the demo end-to-end.

## 6. Demo data

The project already includes JSON fixtures in `quantum_aicp_demo/data/` for products, users, and sample images. The agents load these assets automatically when `AICP_DEMO_MODE` is enabled, so no extra initialization is required for local testing.

## 7. Run the command-line pipeline

Execute the hybrid recommendation pipeline directly from the CLI:

```bash
python -m quantum_aicp_demo.main "Find breathable sustainable sneakers for trail running" --user user_002
```

This prints intents, quantum insights, brand rankings, synthesized scores, and fulfillment routes in JSON format.

## 8. Launch the Streamlit dashboard

Start the demo-friendly dashboard with real-time quantum circuit visualizations and recommendation cards:

```bash
streamlit run quantum_aicp_demo/frontend/streamlit_app.py
```

Then open `http://localhost:8501` in your browser. The dashboard uses mock telemetry in demo mode and toggles to live Azure Quantum integration points when credentials are present.

## 9. Run tests and explore benchmarking hooks

```bash
pytest quantum_aicp_demo/tests -q
```

For lightweight comparisons between classical and quantum-inspired paths, you can interact with helper methods in `QuantumAgent` such as `run_variational_scoring` and `run_kernel_similarity`, or extend `tests/test_pipeline.py` with custom scenarios.

## 10. Docker-based workflow (optional)

Build and run the containerized environment provided in `quantum_aicp_demo/Dockerfile`:

```bash
cd quantum_aicp_demo
docker build -t quantum-aicp-demo .
docker run --rm -p 8501:8501 \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -e AZURE_QUANTUM_SUBSCRIPTION_ID="$AZURE_QUANTUM_SUBSCRIPTION_ID" \
  quantum-aicp-demo
```

The container automatically starts the Streamlit dashboard.

## 11. Troubleshooting tips

- **Missing optional SDKs**: The agents include comprehensive error handling and will log helpful messages if quantum SDKs are absent. Check the console for guidance.
- **Large dependency installs**: If `pip install` takes too long, install heavy quantum packages separately or use the Docker image.
- **Logging verbosity**: Adjust `AICP_LOG_LEVEL` to `DEBUG` for deeper insight into the hybrid quantum-classical pipeline stages.

## 12. Next steps

The architecture is modular and extensible. You can plug in new datasets, tweak quantum model parameters via environment variables, or wire the agents into external services by extending the existing interfaces in `quantum_aicp_demo/agents/`.

Enjoy exploring the Quantum AICP Sneaker Recommendation Engine!
