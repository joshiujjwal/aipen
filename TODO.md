# AIPen — Task Breakdown

## How to Use This File

Workflow per task:
1. **Write failing tests first** (red phase) — never skip this
2. **Implement** until tests pass (green phase)
3. **Review diff manually** — read every line before committing
4. **Commit** with message: `[phase] description — N tests pass`
5. **Update CLAUDE.md / AGENTS.md** if you learned something new (compound loop)
6. **Check evidence gate** before marking a phase complete — all tests must pass + human review

Legend: ⬜ not started · 🔄 in progress · ✅ done · 🚫 blocked

---

## Phase 0: Foundation ⬜

> **Gate**: All tooling installs cleanly, smoke tests pass, CI is green.

- [ ] Initialize pnpm monorepo (`pnpm-workspace.yaml`, root `package.json`)
- [ ] Set up TypeScript config (root `tsconfig.base.json`, per-package extends)
- [ ] ESLint + Prettier config (shared across all TS packages)
- [ ] Set up Vite for `apps/web`
- [ ] Set up `@aipen/shared-types` package with basic `HandwritingJob`, `RecognitionResult` types
- [ ] Set up Python project: `pyproject.toml`, `requirements.txt`, `ruff`, `mypy`, `pytest`
- [ ] FastAPI skeleton in `services/inference` — `/healthz` endpoint, tests pass
- [ ] Express skeleton in `services/api-gateway` — `/healthz` endpoint, tests pass
- [ ] React app skeleton in `apps/web` — renders `<App />`, smoke test passes
- [ ] `docker-compose.yml` for local Postgres + Redis
- [ ] GitHub Actions CI (`.github/workflows/ci.yml`) — lint + test all packages
- [ ] **Review AI config files** (README, CLAUDE.md, AGENTS.md, copilot-instructions.md)

---

## Phase 1: Handwriting Capture + Upload ⬜

> **Gate**: Image/stroke data can be uploaded from the web app and reaches the inference service. Integration test passes.

- [ ] Write integration test: `POST /api/jobs` with a sample PNG → returns job ID (red)
- [ ] `POST /api/jobs` endpoint in API gateway — validates multipart image upload, enqueues Redis job
- [ ] Shared type: `HandwritingJob { id, status, imageUrl, createdAt }`
- [ ] Web app upload component: drag-and-drop + file picker, shows upload progress
- [ ] Write unit tests for upload component (Vitest + Testing Library) (red)
- [ ] Implement upload component until tests pass (green)
- [ ] API gateway forwards job to inference service (HTTP or Redis queue worker)
- [ ] Inference service: `POST /infer` accepts image bytes, runs basic Tesseract OCR
- [ ] Write pytest for `/infer` with sample handwriting fixture images (red then green)
- [ ] Return structured `RecognitionResult { jobId, text, confidence, boundingBoxes[] }`
- [ ] Manual test evidence: upload 5 real handwriting samples, record accuracy in `docs/manual-test-log.md`

---

## Phase 2: ML Model Integration (TrOCR) ⬜

> **Gate**: TrOCR model pipeline replaces Tesseract on printed + cursive samples with measurable accuracy improvement. Benchmarks documented.

- [ ] Write benchmark test harness in `tests/inference/` (red) — loads fixture set, measures WER
- [ ] Integrate `microsoft/trocr-base-handwritten` via HuggingFace Transformers
- [ ] Model loader with lazy init + caching (don't reload on every request)
- [ ] Pre-processing pipeline: image resize, grayscale, contrast normalization
- [ ] Post-processing: strip artefacts, fix common OCR errors, normalize whitespace
- [ ] A/B comparison endpoint: `POST /infer?engine=trocr|tesseract`
- [ ] Confidence scoring — return per-word confidence scores
- [ ] Model versioning: `MODEL_VERSION` env var, log model name in every response
- [ ] Benchmark: run on 50-sample fixture set, record WER in `docs/model-benchmarks.md`
- [ ] **Evidence gate**: WER < 15% on printed samples, < 30% on cursive samples

---

## Phase 3: User Auth + Notes Storage ⬜

> **Gate**: User can sign up, log in, upload handwriting, and retrieve saved notes. Auth tests pass.

- [ ] Write auth integration tests (red): register → login → get protected route → logout
- [ ] `users` and `notes` schema migrations (Drizzle ORM or raw SQL)
- [ ] `POST /auth/register`, `POST /auth/login` → JWT (RS256)
- [ ] Auth middleware in API gateway — validate JWT on protected routes
- [ ] `GET /api/notes`, `GET /api/notes/:id`, `DELETE /api/notes/:id`
- [ ] Web app: login/register pages (React Hook Form + Zod validation)
- [ ] Web app: notes list page — shows recognized text, timestamp, thumbnail
- [ ] Write component tests for notes list and auth forms (red then green)
- [ ] Manual test evidence: full user journey recorded in `docs/manual-test-log.md`

---

## Phase 4: Real-Time Stroke Capture (WebSocket) ⬜

> **Gate**: Live pen strokes are streamed from the web app to the backend over WebSocket, processed incrementally.

- [ ] Design WebSocket message protocol in `packages/shared-types`: `StrokeEvent`, `LiveInferenceChunk`
- [ ] Write WS integration test (red): client sends stroke events → receives partial text updates
- [ ] WebSocket handler in API gateway (`ws://localhost:3001/ws/live`)
- [ ] Streaming inference endpoint in FastAPI: process stroke batches as they arrive
- [ ] Canvas component in web app: captures pointer events → encodes as `StrokeEvent`
- [ ] Live preview panel: renders incremental text as user writes
- [ ] Debounce + buffer strategy (configurable, default 200ms)
- [ ] Manual test evidence: record latency (stroke → text) in `docs/manual-test-log.md`

---

## Phase 5: Export + Integrations ⬜

> **Gate**: Recognized notes can be exported to Markdown, PDF, and copied to clipboard. Tests pass.

- [ ] Export service: `RecognitionResult → Markdown string` (unit tested)
- [ ] Export service: `RecognitionResult → PDF` (via `pdfkit`)
- [ ] `GET /api/notes/:id/export?format=md|pdf` endpoint
- [ ] Web app: export buttons on note detail page
- [ ] Clipboard copy with visual feedback (toast notification)
- [ ] Notion integration stub (OAuth flow placeholder + docs)
- [ ] Write export tests (red then green)

---

## Phase 6: Polish & Harden ⬜

> **Gate**: Error handling is complete, performance acceptable, security review done.

- [ ] Structured logging (Pino in gateway, structlog in Python service)
- [ ] Request tracing: `x-request-id` header propagated across services
- [ ] Rate limiting on API gateway (express-rate-limit)
- [ ] Input validation: max image size (10 MB), supported MIME types, malformed JSON
- [ ] Error boundary in React app — friendly error UI
- [ ] Accessibility audit (axe-core / storybook a11y addon)
- [ ] Bundle size audit (`pnpm build --report`)
- [ ] Security: CSP headers, CORS policy, JWT expiry refresh flow
- [ ] Load test inference service: 10 concurrent requests, p99 < 3 s
- [ ] Dependency audit: `pnpm audit`, `pip-audit`

---

## Phase 7: Ship ⬜

> **Gate**: Deployed to staging, smoke tests pass in production environment.

- [ ] Dockerfiles for inference service + API gateway
- [ ] `docker-compose.prod.yml` with env var injection
- [ ] Staging deploy (Railway / Fly.io / Render) — document steps in `docs/deploy.md`
- [ ] Environment variable documentation (`docs/env-vars.md`)
- [ ] Smoke test suite against staging URL
- [ ] Update README with live demo link

---

## Parking Lot 🅿️

> Ideas that came up but are not in scope yet.

- Handwriting style transfer (generate text in user's handwriting font)
- Offline mode — local inference via ONNX in the browser (WASM)
- Hardware SDK integration (Wacom / Neo smartpen BLE protocol)
- iOS/Android React Native app (Phase 4+ only after web is stable)
- Math equation recognition (MathOCR / Pix2Tex)
- Multi-language OCR (Arabic, CJK scripts)

---

## Lessons Learned 📝

> Update this section as you discover non-obvious truths about the codebase.

_(empty — fill in as you work)_
