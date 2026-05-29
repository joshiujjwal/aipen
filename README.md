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
