# Backend Quick Start

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Run tests

```bash
cd backend
pytest
```
