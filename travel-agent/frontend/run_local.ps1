# PowerShell helper to run frontend (Streamlit) locally
if (-not (Test-Path .venv)) {
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
if (-not (Test-Path ..\.env)) {
    Copy-Item ..\.env.example ..\.env -ErrorAction SilentlyContinue
}
streamlit run app.py --server.port 8501
