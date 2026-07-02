#!/usr/bin/env sh
set -eu

(cd frontend && npm run lint && npm run typecheck)
(cd backend && uv run ruff check . && uv run mypy app && uv run pytest)
