# AIPen 🖊️

> **AI pen handwriting converter** — capture handwriting from a smart pen device, convert it to text/structured data via ML/OCR, and sync to any platform.

![Status](https://img.shields.io/badge/status-🚧_Early_Development-orange)
![Stack](https://img.shields.io/badge/stack-React_·_FastAPI_·_Node.js-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What It Does

AIPen bridges a hardware smart pen with a cloud inference pipeline:

1. **Capture** — pen strokes/images transmitted from hardware (BLE/USB) to the companion app
2. **Infer** — Python + FastAPI inference service runs OCR + ML handwriting recognition
3. **Deliver** — converted text, markdown, or structured data returned to the React web/mobile app
4. **Sync** — notes stored in user workspace, exportable to Notion, Markdown, PDF

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web App | React 18 + TypeScript + Vite |
| Mobile App | React Native (TypeScript) |
| API Gateway | Node.js + Express + TypeScript |
| Inference Service | Python 3.11 + FastAPI + PyTorch / TesseractOCR |
| Shared Types | TypeScript package (`@aipen/types`) |
| Database | PostgreSQL (users, notes) + Redis (job queue) |
| ML Models | TrOCR (HuggingFace) + custom stroke classifier |
| CI/CD | GitHub Actions |

---

## Project Structure

```
aipen/
├── apps/
│   ├── web/                    # React + TypeScript companion web app
│   └── mobile/                 # React Native mobile app (iOS/Android)
├── services/
│   ├── inference/              # Python + FastAPI OCR/ML inference service
│   └── api-gateway/            # Node.js API gateway (auth, routing, ws)
├── packages/
│   └── shared-types/           # Shared TypeScript types/interfaces
├── docs/
│   ├── spec.md                 # Feature specification
│   └── adr/                    # Architecture decision records
├── tests/                      # Integration test suites
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/ci.yml
├── CLAUDE.md                   # Claude AI context
├── AGENTS.md                   # Agent setup + code style
└── TODO.md                     # Evidence-gated task breakdown
```

---

## Getting Started

### Prerequisites

- Node.js ≥ 20, pnpm ≥ 8
- Python 3.11+, uv or pip
- Docker + Docker Compose (for local infra)
- PostgreSQL 15, Redis 7

### Install

```bash
# Clone
git clone https://github.com/joshiujjwal/aipen.git && cd aipen

# Install JS dependencies (monorepo)
pnpm install

# Install Python dependencies
cd services/inference && pip install -r requirements.txt && cd ../..
```

### Dev

```bash
# Start all services (Docker Compose)
docker compose up -d

# Web app
cd apps/web && pnpm dev

# API Gateway
cd services/api-gateway && pnpm dev

# Inference service
cd services/inference && uvicorn app.main:app --reload --port 8000
```

### Test

```bash
# All JS tests
pnpm test

# Inference service tests
cd services/inference && pytest -v

# Web unit tests
cd apps/web && pnpm test

# API gateway tests
cd services/api-gateway && pnpm test
```

### Lint

```bash
pnpm lint          # ESLint across all JS/TS packages
cd services/inference && ruff check . && mypy app/
```

---

## Contributing

1. **Read TODO.md** — pick the next `⬜` task in the current phase
2. **Write tests first** (red phase) — no implementation without failing tests
3. **Implement** until tests pass (green phase)
4. **Review your diff** manually before committing
5. **Commit** with a descriptive message including evidence ("Adds X — N tests pass")
6. **Open a PR** — include test output in the description
7. **Update CLAUDE.md / AGENTS.md** if you discovered a new convention

> Small, focused PRs only. One feature or fix per PR.

---

## Architecture Overview

```
Smart Pen (BLE/USB)
      │
      ▼
[Companion App: React Web / React Native]
      │  REST / WebSocket
      ▼
[API Gateway: Node.js/Express]
      │  HTTP / Job Queue (Redis)
      ▼
[Inference Service: FastAPI + TrOCR]
      │
      ├── OCR pipeline (TesseractOCR fallback)
      ├── Stroke-to-text ML model (TrOCR / custom)
      └── Post-processing (punctuation, formatting)
      │
      ▼
[PostgreSQL: users, notes, recognition jobs]
```

## 🚀 Improvement Proposals

### First-Principles Analysis
- AIPen is a **hardware-dependent software product** — the value proposition collapses without a supported smart pen, yet no concrete device is named.
- The inference pipeline overlaps with existing note-digitization products, so the likely differentiation is cloud sync and LLM-based structuring rather than OCR alone.
- The monorepo with four services introduces substantial complexity before the hardware dependency is even validated.
- Handwriting quality varies widely by user, so baseline model accuracy will likely feel unreliable without personalization.

### Key Risks & Assumptions
- **BLE/USB hardware compatibility is assumed but undefined** — the capture layer is still underspecified.
- **Cloud TrOCR inference may be heavy and slow** — users expect near-immediate recognition from note capture flows.
- **Integration goals like Notion export are more complex than they look** — OAuth, mapping, and rate limits can dominate scope.
- **A separate mobile app doubles product surface area too early** — validation may be possible without it.

### Concrete Improvement Ideas
1. **Name and test against one specific pen** — pick a real device and document the protocol so the capture path becomes concrete.
2. **Build a pen-agnostic image-upload mode first** — validate OCR, structuring, and export flows without waiting on hardware.
3. **Evaluate on-device inference** — reduce latency and improve privacy by exploring quantized local models.
4. **Scope the MVP to web-only** — delay React Native until the core pipeline works reliably.
5. **Add a per-user handwriting calibration flow** — this is likely the biggest lever on recognition quality and retention.
