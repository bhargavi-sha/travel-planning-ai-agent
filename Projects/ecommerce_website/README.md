# ShopSphere

Amazon-inspired e-commerce demo with independent FastAPI and React projects.

## Run backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

API: `http://localhost:8000/api/products`

## Run frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:5173`).
