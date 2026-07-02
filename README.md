# MongoDB Decision Intelligence Platform

Production-ready monorepo scaffold for a Next.js frontend and FastAPI backend backed by MongoDB.

This repository intentionally contains only platform wiring, health checks, configuration, and placeholder pages. Business logic should be added behind explicit API and domain boundaries.

## Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- Backend: FastAPI, Python 3.12, uv, Motor, Pydantic
- Data: MongoDB
- Runtime: Docker Compose

## Repository Layout

```text
frontend/              Next.js application
backend/               FastAPI application
docs/                  Architecture and operational docs
docker/                Dockerfiles and container support
scripts/               Developer utility scripts
sample_data/           Non-production sample fixtures
.github/workflows/    CI automation
```

## Quick Start

1. Copy environment defaults:

   ```bash
   cp .env.example .env
   ```

2. Start the stack:

   ```bash
   docker compose up --build
   ```

3. Open the apps:

   - Frontend: <http://localhost:3000>
   - Backend health: <http://localhost:8000/health>
   - API docs: <http://localhost:8000/docs>

## Local Development

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Backend:

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```

## Quality Gates

Frontend:

```bash
cd frontend
npm run lint
npm run typecheck
```

Backend:

```bash
cd backend
uv run ruff check .
uv run mypy app
uv run pytest
```

## Environment

Use `.env.example` as the source of documented configuration. Do not commit secrets or production credentials.
