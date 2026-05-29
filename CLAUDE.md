# CLAUDE.md — AIPen Context

> Keep this file under 200 lines. Update it when you discover a non-obvious convention.
> This file tells Claude what it cannot infer from the code itself.

---

## Quick Start (run these first, every session)

```bash
# 1. Run all tests to see current baseline
pnpm test                                      # JS/TS across all packages
cd services/inference && pytest -v && cd ../..  # Python inference tests

# 2. Check what's next
cat TODO.md | grep -A2 "⬜"
```

## Commands

### JS / TypeScript (pnpm monorepo)

```bash
pnpm install              # Install all packages
pnpm dev                  # Start all dev servers (turbo)
pnpm build                # Build all packages
pnpm test                 # Run all tests (vitest + jest)
pnpm lint                 # ESLint across all packages
pnpm format               # Prettier format
pnpm typecheck            # tsc --noEmit across all packages

# Per-package
cd apps/web && pnpm dev           # Vite on :5173
cd services/api-gateway && pnpm dev  # ts-node-dev on :3001
```

### Python (inference service)

```bash
cd services/inference
uvicorn app.main:app --reload --port 8000   # Dev server
pytest -v                                   # All tests
pytest tests/test_infer.py -v -k "test_name"  # Single test
ruff check .                                # Linter
ruff format .                               # Formatter
mypy app/                                   # Type check
```

### Docker

```bash
docker compose up -d          # Start Postgres + Redis
docker compose logs -f        # Watch logs
docker compose down           # Stop
```

---

## Directory Map

```
apps/web/src/
  components/    Reusable UI (Button, Card, Toast — no business logic)
  pages/         Route-level components (one file per route)
  hooks/         Custom React hooks (useUpload, useNotes, useWebSocket)
  lib/           API client, WebSocket client, export helpers
  types/         Local TS types (re-exports from @aipen/types)

services/inference/app/
  routers/       FastAPI route handlers (infer.py, health.py)
  models/        ML model loaders — lazy init, singleton pattern
  utils/         Pre/post-processing pipelines, image helpers

services/api-gateway/src/
  routes/        Express route handlers (jobs, notes, auth)
  middleware/    Auth middleware, error handler, rate limiter

packages/shared-types/src/
  index.ts       All exported types and Zod schemas — source of truth

tests/
  inference/     pytest integration tests for FastAPI
  api-gateway/   Supertest integration tests
  web/           Playwright e2e tests (Phase 3+)
```

---

## Conventions & Gotchas

### TypeScript

- **Zod is the schema layer** — all API request/response shapes are validated with Zod schemas in `@aipen/types`. Do not add ad-hoc validation elsewhere.
- `shared-types` is a dev dependency in all packages — import as `@aipen/types`
- Use `import type` for type-only imports everywhere
- No `any` — use `unknown` and narrow explicitly
- Express route handlers must be typed `RequestHandler` — no inline `(req, res) =>` without typing

### Python (FastAPI / inference)

- Models are **singletons** — instantiate once in `app/models/` with `@lru_cache` or module-level global; never re-load per request
- All inference functions must accept `PIL.Image` objects, not file paths — callers handle I/O
- Use `async def` for FastAPI route handlers; use `run_in_executor` for blocking torch inference calls
- Pydantic v2 — use `model_validate` not `.parse_obj()`
- `ruff` replaces flake8, isort, and black — run `ruff format .` not `black .`

### React

- **No Redux** — React Query (`@tanstack/react-query`) for server state, `useState`/`useContext` for local UI state
- Canvas stroke capture uses `PointerEvent`, not `MouseEvent` (supports stylus pressure)
- WebSocket connection lives in `useWebSocket` hook — never open WS inside a component directly

### Testing

- **Red before green** — commit the failing test first, then implement
- Inference fixture images live in `tests/inference/fixtures/` — add `.expected.txt` alongside each image
- Do not mock the ML model in integration tests — use the real model with a known fixture
- Snapshot tests are banned — they hide bugs

### Database

- Migrations are plain SQL in `services/api-gateway/migrations/` — numbered `0001_init.sql`
- Never alter a migration that's already run in any environment — always add a new migration
- Soft deletes: set `deleted_at`, never `DELETE` user-owned data immediately

---

## Workflow (every task)

1. `git status` — confirm clean working tree
2. `pnpm test && pytest -v` — confirm baseline passing
3. Write failing test (red) — commit it: `test: failing test for <feature>`
4. Implement until green — commit: `feat: <feature> — N tests pass`
5. Refactor if needed — tests must stay green
6. `pnpm lint && ruff check .` — fix all warnings
7. Update this file if you discovered something new
8. Open PR with test output pasted in description

---

## Environment Variables

See `docs/env-vars.md` (TODO — create in Phase 0).

Key vars:
- `DATABASE_URL` — Postgres connection string
- `REDIS_URL` — Redis connection string
- `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` — RS256 keys (base64 encoded)
- `MODEL_VERSION` — TrOCR model tag (default: `microsoft/trocr-base-handwritten`)
- `MAX_IMAGE_SIZE_MB` — default `10`
- `INFERENCE_SERVICE_URL` — gateway → inference service URL
