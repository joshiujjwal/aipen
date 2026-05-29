# GitHub Copilot Instructions — AIPen

## Project Overview

AIPen is an AI handwriting converter: a React + TypeScript web app, a Node.js/Express API gateway, and a Python + FastAPI ML inference service (TrOCR + Tesseract). It converts handwriting images and live pen strokes into digital text.

## Stack

| Layer | Tech |
|---|---|
| Frontend | React 18, TypeScript, Vite, Tailwind CSS, Tanstack Query |
| API Gateway | Node.js 20, Express 5, TypeScript, Drizzle ORM, Zod |
| Inference | Python 3.11, FastAPI, PyTorch, HuggingFace Transformers, Tesseract |
| Shared Types | `@aipen/types` — Zod schemas + TypeScript interfaces |
| DB | PostgreSQL 15 |
| Queue | Redis (BullMQ) |

## Coding Conventions

### TypeScript / React

- Named exports preferred over default exports (exception: route-level pages)
- All API shapes live in `packages/shared-types/src/index.ts` — never define inline interfaces for API data
- Use `import type` for type-only imports
- React state: `@tanstack/react-query` for server state; `useState` / `useContext` for local UI state
- No Redux. No MobX.
- Custom hooks live in `apps/web/src/hooks/`, prefixed `use`
- Tailwind for all styling — no CSS modules, no inline `style={}`
- Canvas stroke events must use `PointerEvent` (not `MouseEvent`) to support stylus pressure
- Zod schemas named `<Type>Schema`, co-located with their TypeScript type

### Python

- `ruff format` is the formatter (not black)
- All functions and methods require type annotations
- FastAPI route handlers are `async def`; blocking calls (torch inference) use `asyncio.run_in_executor`
- ML models are singletons — instantiated once at module level or with `@lru_cache`
- Use Pydantic v2: `model_validate()` not `.parse_obj()`
- Never pass raw file paths into inference functions — callers provide `PIL.Image` objects

## Testing Conventions

- **Write the failing test first.** Always.
- Test file mirrors source: `app/utils/preprocess.py` → `tests/test_preprocess.py`
- Fixture handwriting images live in `tests/inference/fixtures/` with matching `.expected.txt`
- Vitest for React components (Testing Library for DOM assertions)
- Supertest for Express endpoints
- pytest for all Python code
- **Snapshot tests are banned** — they hide real bugs
- Do not mock the ML model in integration tests — use the real model + fixtures

## Boundaries

- **Do not refactor** working code unless the user explicitly asks
- **Do not remove** existing passing tests
- **Do not add** `console.log` / `print` debug statements in committed code — use structured loggers
- **Do not** use `any` in TypeScript — use `unknown` and narrow explicitly
- **Do not** define new DB schemas outside of the SQL migration files in `services/api-gateway/migrations/`
- When adding a new endpoint, always update `packages/shared-types/src/index.ts` first
- When adding a new Python function with ML inference, benchmark it with the fixture dataset and record WER in `docs/model-benchmarks.md`
