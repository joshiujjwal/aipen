# AGENTS.md — AIPen

> Standard setup + coding conventions for AI coding agents (OpenAI Codex, GitHub Copilot Workspace, etc.)

---

## Setup

```bash
# 1. Install all dependencies
pnpm install
cd services/inference && pip install -r requirements.txt && cd ../..

# 2. Start local infrastructure
docker compose up -d   # Postgres :5432, Redis :6379

# 3. Verify everything works
pnpm test
cd services/inference && pytest -v && cd ../..
```

---

## Repository Layout

```
apps/web/          React 18 + TypeScript (Vite, Vitest, Testing Library)
apps/mobile/       React Native TypeScript (placeholder, Phase 4+)
services/inference/  Python 3.11, FastAPI, PyTorch, TrOCR, Tesseract
services/api-gateway/ Node.js 20, Express, TypeScript, Drizzle ORM
packages/shared-types/ Shared TypeScript types + Zod schemas
tests/             Integration + e2e test suites
docs/              spec.md, adr/, model benchmarks, deploy guide
```

---

## Code Style

### TypeScript / JavaScript

- **Formatter**: Prettier (config in root `.prettierrc`)
- **Linter**: ESLint with `@typescript-eslint` (config in root `eslint.config.mjs`)
- **Imports**: absolute imports aliased from `src/` (e.g. `@/components/Button`)
- Prefer `const` over `let`; never `var`
- Prefer `async/await` over `.then()` chains
- Prefer named exports over default exports (exception: page-level components)
- All public API interfaces go in `packages/shared-types/src/index.ts`
- Zod schemas are co-located with their types as `<TypeName>Schema`
- No commented-out code in commits

### Python

- **Formatter**: `ruff format` (replaces black + isort)
- **Linter**: `ruff check` + `mypy` (strict mode)
- All functions have type annotations
- Docstrings on public functions (Google style)
- `dataclasses` or Pydantic models for structured data — no plain dicts across module boundaries
- Tests in `tests/` directory, file names `test_*.py`, function names `test_*`

### React

- Components are function components only — no class components
- Props interfaces named `<ComponentName>Props`
- Custom hooks prefixed `use` and live in `apps/web/src/hooks/`
- No inline styles — use Tailwind CSS utility classes
- Accessible by default: all interactive elements have ARIA labels or visible labels

---

## Testing

### Philosophy: Red → Green → Refactor

1. **Always write the failing test first.** No exceptions.
2. Run the test, confirm it fails for the right reason.
3. Implement the minimal code to make it pass.
4. Refactor while keeping tests green.
5. Commit both test + implementation together.

### Commands

```bash
# JS/TS unit tests (Vitest)
cd apps/web && pnpm test
cd services/api-gateway && pnpm test

# Python unit + integration tests
cd services/inference && pytest -v

# Integration tests (requires running Docker infra)
pnpm test:integration

# Type checking (must pass before PR)
pnpm typecheck
cd services/inference && mypy app/
```

### Rules

- Do not mock the inference ML model in integration tests — use real model with fixture images
- Snapshot tests are **banned** — they hide bugs
- Test file mirrors source file: `src/lib/export.ts` → `tests/lib/export.test.ts`
- Minimum coverage targets (enforced in CI): 80% lines for inference service, 70% for gateway

---

## PR Instructions

1. **Title format**: `[phase] Short description` (e.g. `[phase1] Add image upload endpoint`)
2. **Description must include**:
   - What changed and why
   - Test output (paste the relevant `pytest -v` or `pnpm test` output)
   - Manual test evidence (screenshot or curl output) for any user-facing change
3. **Do not**:
   - Combine multiple features in one PR
   - Remove existing tests without a comment explaining why
   - Introduce `TODO` comments without a corresponding TODO.md entry
   - Merge without all CI checks green

---

## Common Tasks

### Add a new API endpoint (gateway)

1. Add the Zod request/response schemas to `packages/shared-types/src/index.ts`
2. Write integration test in `tests/api-gateway/` (red)
3. Add route handler in `services/api-gateway/src/routes/`
4. Register route in `services/api-gateway/src/app.ts`
5. Run `pnpm typecheck` — fix all errors
6. Make test pass (green)

### Add a new inference feature

1. Add fixture image + `.expected.txt` to `tests/inference/fixtures/`
2. Write pytest (red)
3. Implement in `services/inference/app/`
4. Ensure `mypy app/` is clean
5. Run benchmark: document WER in `docs/model-benchmarks.md`

### Add a new React component

1. Create component file in `apps/web/src/components/<ComponentName>.tsx`
2. Write Vitest + Testing Library test (red)
3. Implement component (green)
4. Export from `apps/web/src/components/index.ts`
