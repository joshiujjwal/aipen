# AIPen — Feature Specification

**Version**: 0.1.0-draft  
**Status**: 🚧 Draft  
**Last updated**: 2025

---

## 1. Overview

### Problem Statement

Handwritten notes are difficult to search, share, or integrate with digital workflows. Existing OCR tools are either desktop-only, low accuracy on cursive, or don't accept real-time stroke input. AIPen solves this by providing a companion app + cloud inference pipeline that converts handwriting (from a smart pen or scanned image) into editable, structured digital text — in real time.

### Goals

- Convert handwriting images/stroke data to text with ≥ 85% word-level accuracy on clean samples
- Support real-time streaming (latency ≤ 500 ms from last stroke to first text result)
- Provide a clean, responsive web app as the primary UI
- Store and sync converted notes to user accounts
- Allow export to Markdown and PDF

### Non-Goals (v1)

- Firmware / BLE SDK for physical hardware (out of scope — hardware agnostic)
- Offline-only inference (cloud-first in v1)
- Math/formula recognition
- Mobile native app (React Native planned for Phase 4+)

---

## 2. Functional Requirements

### 2.1 Handwriting Upload & Job Processing

- [ ] User can upload a PNG/JPG/TIFF image via drag-and-drop or file picker
- [ ] System accepts images up to 10 MB; returns `400` with clear message for oversized files
- [ ] Upload creates a `HandwritingJob` record with status `pending`
- [ ] Job is processed asynchronously; status transitions: `pending → processing → done | failed`
- [ ] User sees real-time job status updates (WebSocket or polling fallback)
- [ ] Completed job returns `RecognitionResult` with full text and per-word confidence scores

### 2.2 Real-Time Stroke Input

- [ ] Web app provides a canvas for live pen input (mouse/stylus via Pointer Events API)
- [ ] Strokes are batched and sent via WebSocket every 200 ms (configurable)
- [ ] Inference service returns incremental text chunks as strokes arrive
- [ ] User sees live text preview updating as they write

### 2.3 ML / OCR Inference

- [ ] Inference service supports two engines, selectable per-request: `tesseract` (fast fallback) and `trocr` (high accuracy)
- [ ] Default engine: `trocr`
- [ ] Pre-processing pipeline: resize to ≤ 1024px width, convert to grayscale, apply CLAHE contrast enhancement
- [ ] Post-processing: strip stray characters, normalize whitespace, capitalize first word of sentences
- [ ] Response includes: `{ text, words: [{ word, confidence, bbox }], engine, modelVersion, processingMs }`

### 2.4 User Authentication

- [ ] Register with email + password (bcrypt, cost factor 12)
- [ ] Login returns JWT (RS256, 15 min access token + 7 day refresh token)
- [ ] Refresh token rotation on every use
- [ ] All note endpoints require valid access token

### 2.5 Notes Management

- [ ] Notes are persisted per user: `{ id, userId, title, rawText, imageUrl, createdAt, updatedAt }`
- [ ] `GET /api/notes` — paginated list (20 per page), sorted by `createdAt DESC`
- [ ] `GET /api/notes/:id` — full note detail including recognition metadata
- [ ] `DELETE /api/notes/:id` — soft delete (mark deleted, don't purge immediately)
- [ ] Notes are full-text searchable via `GET /api/notes?q=<query>`

### 2.6 Export

- [ ] Export note as Markdown: `GET /api/notes/:id/export?format=md`
- [ ] Export note as PDF: `GET /api/notes/:id/export?format=pdf`
- [ ] Copy-to-clipboard from web UI

---

## 3. Non-Functional Requirements

- [ ] API response time ≤ 200 ms (p99) for CRUD endpoints (excluding inference)
- [ ] Inference time ≤ 3 s (p99) for a single A4 page image
- [ ] Live stroke latency (stroke → first text chunk) ≤ 500 ms
- [ ] 99.5% uptime SLA for API gateway
- [ ] GDPR-compliant: user can delete all data via `DELETE /api/account`
- [ ] All API communication over HTTPS/WSS
- [ ] Images stored encrypted at rest (S3 SSE-S3 or equivalent)

---

## 4. Data Model

### `users`

```sql
CREATE TABLE users (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now(),
  deleted_at  TIMESTAMPTZ
);
```

### `handwriting_jobs`

```sql
CREATE TABLE handwriting_jobs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES users(id),
  status      TEXT NOT NULL DEFAULT 'pending',  -- pending|processing|done|failed
  image_url   TEXT,
  engine      TEXT DEFAULT 'trocr',
  created_at  TIMESTAMPTZ DEFAULT now(),
  updated_at  TIMESTAMPTZ DEFAULT now()
);
```

### `notes`

```sql
CREATE TABLE notes (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id),
  job_id        UUID REFERENCES handwriting_jobs(id),
  title         TEXT,
  raw_text      TEXT,
  word_data     JSONB,       -- array of { word, confidence, bbox }
  image_url     TEXT,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now(),
  deleted_at    TIMESTAMPTZ
);
CREATE INDEX notes_user_fts ON notes USING gin(to_tsvector('english', raw_text));
```

---

## 5. API Design

### API Gateway (Node.js, port 3001)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | — | Register new user |
| POST | `/auth/login` | — | Login, returns tokens |
| POST | `/auth/refresh` | — | Rotate refresh token |
| POST | `/api/jobs` | ✅ | Upload image, create job |
| GET | `/api/jobs/:id` | ✅ | Get job status |
| GET | `/api/notes` | ✅ | List notes (paginated) |
| GET | `/api/notes/:id` | ✅ | Get note detail |
| DELETE | `/api/notes/:id` | ✅ | Soft delete note |
| GET | `/api/notes/:id/export` | ✅ | Export (`?format=md\|pdf`) |
| DELETE | `/api/account` | ✅ | Delete user + all data |
| GET | `/healthz` | — | Health check |
| WS | `/ws/live` | ✅ | Live stroke streaming |

### Inference Service (Python FastAPI, port 8000)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/infer` | Image → recognition result |
| POST | `/infer/stream` | WebSocket: stroke batches → text chunks |
| GET | `/healthz` | Health check + model status |
| GET | `/models` | List loaded models + versions |

---

## 6. TypeScript Shared Types (`@aipen/types`)

```typescript
export type JobStatus = 'pending' | 'processing' | 'done' | 'failed';
export type InferenceEngine = 'trocr' | 'tesseract';

export interface HandwritingJob {
  id: string;
  userId: string;
  status: JobStatus;
  imageUrl?: string;
  engine: InferenceEngine;
  createdAt: string;
  updatedAt: string;
}

export interface WordResult {
  word: string;
  confidence: number;    // 0–1
  bbox: [number, number, number, number];  // x, y, w, h (pixels)
}

export interface RecognitionResult {
  jobId: string;
  text: string;
  words: WordResult[];
  engine: InferenceEngine;
  modelVersion: string;
  processingMs: number;
}

export interface Note {
  id: string;
  userId: string;
  jobId: string;
  title: string;
  rawText: string;
  wordData: WordResult[];
  imageUrl?: string;
  createdAt: string;
  updatedAt: string;
}

export interface StrokeEvent {
  sessionId: string;
  x: number;
  y: number;
  pressure: number;
  timestamp: number;
  isLiftOff: boolean;
}

export interface LiveInferenceChunk {
  sessionId: string;
  partialText: string;
  isFinal: boolean;
}
```

---

## 7. Test Plan

### Unit Tests

| Module | What to test |
|--------|-------------|
| `@aipen/types` | Type guards, validators (Zod schemas) |
| Inference service | Pre-processing pipeline (resize, grayscale, contrast) |
| Inference service | Post-processing (whitespace normalization, capitalization) |
| Inference service | `/infer` with fixture images — known expected outputs |
| API gateway | JWT generation + validation |
| API gateway | Job creation, status transitions |
| API gateway | Note CRUD endpoint handlers |
| Web app | UploadComponent renders, accepts files, calls API |
| Web app | NotesList renders paginated results |
| Web app | Canvas captures stroke events and emits StrokeEvent |

### Integration Tests

| Scenario | Steps |
|----------|-------|
| Upload → OCR | POST image → poll job → verify recognized text |
| Live stroke | Open WS → send StrokeEvents → receive LiveInferenceChunk |
| Auth flow | Register → Login → Access protected endpoint → Refresh → Logout |
| Export | GET /api/notes/:id/export?format=md → valid markdown |

### Fixture Dataset

- Minimum 20 images in `tests/inference/fixtures/`:
  - 5 printed text samples (easy baseline)
  - 5 neat cursive samples
  - 5 messy cursive samples
  - 5 mixed printed + cursive
- Expected text for each fixture stored in `tests/inference/fixtures/*.expected.txt`
- Benchmark: WER (Word Error Rate) reported per category

### Edge Cases

- [ ] Empty canvas (no strokes) — returns empty string, not error
- [ ] All-whitespace image — returns empty string
- [ ] Image with only symbols/numbers — returns them correctly
- [ ] Very small image (< 50×50 px) — returns graceful error
- [ ] Unsupported MIME type — `400 Unsupported file type`
- [ ] File > 10 MB — `413 Payload Too Large`
- [ ] Expired JWT — `401 Unauthorized`
- [ ] Non-owner accessing note — `403 Forbidden`

---

## 8. Open Questions

- [ ] Which BLE pen protocol to support first? (Wacom? Neo Smartpen? Generic HID?)
- [ ] Should stroke data be stored permanently or only the final recognized text?
- [ ] Self-hosted TrOCR vs. OpenAI Vision API as fallback — cost trade-off?
- [ ] Multi-page document support (Phase 2+)?
- [ ] How to handle mixed-language notes?
