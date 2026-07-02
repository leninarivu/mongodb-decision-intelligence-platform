#!/usr/bin/env sh
set -eu

if [ ! -f .env ]; then
  cp .env.example .env
fi

if command -v npm >/dev/null 2>&1; then
  (cd frontend && npm install)
fi

if command -v uv >/dev/null 2>&1; then
  (cd backend && uv sync)
fi

printf '%s\n' 'Bootstrap complete.'
