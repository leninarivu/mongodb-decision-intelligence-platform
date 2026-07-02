# Development

## Prerequisites

- Node.js 20.18 or newer
- Python 3.12
- uv
- Docker Desktop or a compatible Docker runtime

## Environment

Create local configuration from the checked-in template:

```bash
cp .env.example .env
```

## Docker

```bash
docker compose up --build
```

## Local Services

Run services directly when iterating on one layer:

```bash
cd frontend
npm install
npm run dev
```

```bash
cd backend
uv sync
uv run fastapi dev app/main.py
```
