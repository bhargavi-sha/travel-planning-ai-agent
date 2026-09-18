Travel Agent — Agentic AI Travel Planner

Overview
--------
This project implements an agentic travel planning application with a Python/FastAPI backend and a Streamlit frontend. It supports demo mode when external API keys are missing.

Quickstart
----------
1. Copy the example env: `cp .env.example .env` and edit keys (do NOT commit `.env`).

Run with Docker (optional):

```bash
docker compose up --build
```

Run locally without Docker (Windows / PowerShell):

Backend (create a venv, install deps, and run):

```powershell
# from project root
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env -ErrorAction SilentlyContinue
# Edit .env to add API keys if needed, or set DEMO_MODE=true
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend (Streamlit):

```powershell
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example ..\.env -ErrorAction SilentlyContinue
streamlit run app.py --server.port 8501
```

Environment variables (PowerShell examples):

```powershell
# Set GROQ key for current session
$env:GROQ_API_KEY = "<YOUR_KEY>"
# Or create a local .env file and ensure .env is in .gitignore
```

Demo mode
---------
If `DEMO_MODE=true` in your `.env`, the application uses deterministic demo providers and does not call paid APIs. The UI will clearly show "Demo mode — travel data is simulated." Do NOT paste real API keys into shared files or commit them.
