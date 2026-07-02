# Architecture

## Overview

The monorepo separates the product surface from the API runtime:

- `frontend/` contains the Next.js 15 application shell.
- `backend/` contains the FastAPI service, configuration, health endpoint, and MongoDB connection layer.
- `docker/` contains production-oriented container definitions used by `docker-compose.yml`.

## Runtime Flow

1. The browser loads the Next.js app from the frontend container.
2. The frontend reads `NEXT_PUBLIC_API_BASE_URL` for API calls.
3. FastAPI initializes a Motor client during application lifespan startup.
4. `/health` verifies MongoDB availability via `ping`.

## Boundary Rules

- Keep business logic out of route handlers once domains are introduced.
- Keep persistence details behind repository or service modules.
- Keep environment-specific values in `.env` or deployment secrets.
