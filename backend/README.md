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

Auto Swagger docs (like SpringDoc) at http://localhost:8000/docs
