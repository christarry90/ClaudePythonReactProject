# Backend (FastAPI)

You build this during **Milestone 2**. It starts empty on purpose — you write every line.

## Java mental model

Think Spring Boot: `router → service → repository`, DTOs (Pydantic models), DI (`Depends` ≈ `@Autowired`).

## Setup (Milestone 0 / 2)

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run (once you have an app.py)

```bash
uvicorn app:app --reload
```

Auto Swagger docs (like SpringDoc):
- Local Windows setup: http://localhost:8000/docs
- Browser-based environment: `https://<the-domain-you're-on>/proxy/8000/docs` (code-server proxies
  the port for you — same idea as the frontend dev server, see `frontend/README.md`)

## CORS (Milestone 4)

Once the frontend calls this API, add CORS middleware. It's needed for the **local Windows
setup** (frontend and backend run on different ports, so the browser treats them as different
origins) — harmless to include in the browser-based environment too, where both are proxied
through the same origin and CORS doesn't actually apply:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(CORSMiddleware, allow_origins=["*"])
```
