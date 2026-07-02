# Backend

FastAPI backend scaffold using Python 3.12, uv, Motor, and Pydantic.

## Commands

```bash
uv sync
uv run fastapi dev app/main.py
uv run ruff check .
uv run mypy app
uv run pytest
```

## Endpoints

- `GET /health` returns service and MongoDB connectivity status.
