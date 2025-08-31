# CppNB — System Architecture & Design

**Tagline:** Interactive Notebooks for C++ — experiment, compile, and run code cells with ease.

---

## 1) Goals & Non-Goals

### Goals
- Provide a safe, interactive, multi-cell C++ execution environment on the web.
- Support single-cell and multi-cell compilation/execution with per-cell outputs.
- Persist and round-trip notebooks via a custom `.cppnb` JSON format.
- Enforce strong sandboxing (Docker) for untrusted code.
- Be demo-ready on Appwrite’s deployment service.

### Non-Goals (initial)
- Rich UI/UX or collaborative editing beyond basic real-time (stretch).
- Full package manager / build system integration.
- Language support beyond C++ (future: C, CMake, etc.).

---

## 2) High-Level Architecture

```
+-------------------+         HTTPS          +-------------------+      gRPC/HTTPS      +-----------------------+
|   Frontend (Web)  |  <------------------>  |  API Service      |  <--------------->   | Execution Microservice |
| Next.js + Monaco  |                        | FastAPI (Python)  |                     | Sandbox Orchestrator   |
+-------------------+                        +-------------------+                     +-----------+-----------+
        |  Upload/Download .cppnb                        |  CRUD, Orchestrate Execution                      |
        |                                                v                                                   |
        |                                     +-------------------+                                         |
        |                                     |  SQLite Database  |  (Users, Notebooks, Exec logs)          |
        |                                     +-------------------+                                         |
        |                                                                                                   |
        |                                                                                                   v
        |                                                                                           +---------------+
        |                                                                                           | Docker Engine |
        |                                                                                           |  (sandboxed)  |
        |                                                                                           +---------------+
```

**Key separation:** API Service manages notebooks and orchestration; Execution Microservice owns sandboxing and process control.

---

## 3) Component Responsibilities

### Frontend (Next.js)
- Notebook UI: cell list, add/remove/reorder, type selector (`.cpp/.h`).
- Monaco Editor for per-cell code editing.
- Run Single / Run Selected / Run All actions.
- Upload/download `.cppnb` files.
- Display stdout/stderr/exit status per execution.

### API Service (FastAPI)
- REST endpoints for authentication (optional), notebook CRUD, `.cppnb` import/export.
- Validates payloads, enforces quotas and rate limits.
- Orchestrates execution: bundles selected cells, calls Execution Microservice, streams results back.
- Persists notebooks, users, and execution logs to SQLite.

### Execution Microservice
- Stateless service that receives an execution spec (files + options).
- Creates a temp workspace; writes files; invokes Docker to compile/run.
- Applies resource limits: memory, CPU, wall-clock timeout, no network.
- Captures stdout/stderr/exit code; cleans up workspace; returns results.

### Database (SQLite)
- Users (optional), Notebooks, Cells, ExecutionLogs.
- Simple relational schema; easy to migrate to Postgres later.

---

## 4) Data Model & Storage

### 4.1 Relational Schema (SQLite)

**users** (optional)
- id (PK, uuid)
- email (unique)
- password_hash (if self-auth) or provider_id (if external)
- created_at, updated_at

**notebooks**
- id (PK, uuid)
- owner_id (FK users.id, nullable if no auth)
- name (text)
- metadata_json (json)
- created_at, updated_at

**cells**
- id (PK, uuid)
- notebook_id (FK notebooks.id)
- position (int)  — for ordering
- filename (text)
- type (enum: 'source'|'header')
- code (text)
- created_at, updated_at

**execution_logs**
- id (PK, uuid)
- notebook_id (FK notebooks.id)
- cell_ids (text/json array)
- flags (text)  — compiler flags used
- stdout (text)
- stderr (text)
- exit_code (int)
- status (enum: success|compile_error|runtime_error|timeout)
- duration_ms (int)
- created_at

> Note: We also support file-based `.cppnb` round-trip. The DB stores the live state; export/import maps to/from the DB.

### 4.2 `.cppnb` File (JSON) — Versioned

```json
{
  "version": "1.0",
  "notebook_name": "My First Notebook",
  "created_at": "2025-08-28T12:00:00Z",
  "updated_at": "2025-08-28T12:30:00Z",
  "metadata": { "author": "Ayush", "language": "C++17" },
  "cells": [
    { "id": "cell-1", "type": "source", "filename": "main.cpp", "code": "...", "outputs": [] },
    { "id": "cell-2", "type": "header", "filename": "utils.h", "code": "...", "outputs": [] }
  ],
  "execution_groups": [
    { "id": "group-1", "name": "Main with Utils", "cell_ids": ["cell-1","cell-2"],
      "last_run": "2025-08-28T12:20:00Z",
      "outputs": { "stdout": "...", "stderr": "", "exit_code": 0, "status": "success" } }
  ]
}
```

---

## 5) API Design (REST)

### 5.1 Notebook CRUD
- `POST /api/notebooks` — create
  - Body: `{ name, metadata? }`
  - Res: `{ id, name, created_at }`
- `GET /api/notebooks/{id}` — fetch notebook with cells
  - Res: `{ id, name, metadata, cells: [...] }`
- `PUT /api/notebooks/{id}` — update metadata/name
- `DELETE /api/notebooks/{id}` — delete notebook and cells
- `POST /api/notebooks/{id}/cells` — add cell
  - Body: `{ position?, type, filename, code }`
- `PUT /api/cells/{cellId}` — update cell (filename/type/code/position)
- `DELETE /api/cells/{cellId}` — remove cell
- `POST /api/notebooks/{id}/export` — returns `.cppnb` file
- `POST /api/notebooks/import` — upload `.cppnb` to create notebook

### 5.2 Execution
- `POST /api/execute`
  - Body:
    ```json
    {
      "notebook_id": "...",            
      "cell_ids": ["...","..."],      
      "flags": ["-std=c++17","-O2"],
      "stdin": "optional input"        
    }
    ```
  - Res:
    ```json
    {
      "stdout": "...",
      "stderr": "...",
      "exit_code": 0,
      "status": "success|compile_error|runtime_error|timeout",
      "duration_ms": 423
    }
    ```

> The API Service validates `cell_ids`, fetches cells, and forwards an **Execution Spec** to the Execution Microservice.

### 5.3 Health/Meta
- `GET /api/health` — liveness probe
- `GET /api/version` — build info

---

## 6) Execution Microservice Contract

### Request (from API Service)
`POST /run`
```json
{
  "files": [
    { "name": "main.cpp", "type": "source", "content": "..." },
    { "name": "utils.h", "type": "header", "content": "..." }
  ],
  "entry": "auto",                 
  "flags": ["-std=c++17","-O2"],  
  "limits": { "cpu": 0.5, "memory_mb": 256, "timeout_sec": 5 },
  "stdin": "optional input"
}
```

### Response
```json
{
  "stdout": "...",
  "stderr": "...",
  "exit_code": 0,
  "status": "success|compile_error|runtime_error|timeout",
  "duration_ms": 423
}
```

### Behavior
1. Create temp dir; write files.
2. Build compile command: `g++ *.cpp -o program [flags]` (headers are included if referenced).
3. Run in Docker container with flags:
   - `--rm --network=none --cpus=0.5 --memory=256m --pids-limit=128`
   - Bind mount temp dir to `/work`.
4. Execute with wall-clock timeout (kill container if exceeded).
5. Capture outputs; cleanup; return JSON.

---

## 7) Security Model
- **Process Isolation:** Each run in a fresh Docker container.
- **Resource Limits:** CPU, memory, PID count, file descriptors, execution timeout.
- **Network Isolation:** `--network=none` to prevent egress.
- **Filesystem:** Bind-mounted temp dir; read-only base image; no host paths exposed.
- **Input Sanitization:** Validate filenames, forbid path traversal, limit file sizes.
- **Rate Limiting:** Per-IP or per-user limits at API Service (e.g., 30 runs/min).

---

## 8) Error Handling & Status Codes
- 400 — invalid payload (bad cell IDs, too-large files).
- 429 — rate limit exceeded.
- 500 — internal errors (compilation service unreachable).
- Execution statuses: `success`, `compile_error`, `runtime_error`, `timeout`.

**User-facing messages:**
- Compile errors show first N lines of stderr + hint to open full logs.
- Timeouts show message with current limits; suggest reducing input/loops.

---

## 9) Sequence Diagrams (Textual)

### Run Selected Cells
```
User -> Frontend: Click "Run Selected"
Frontend -> API: POST /api/execute { notebook_id, cell_ids, flags }
API -> DB: SELECT cells WHERE id IN (...)
API -> ExecSvc: POST /run { files:[...], flags, limits }
ExecSvc -> Docker: run gcc image (compile + run)
Docker -> ExecSvc: stdout/stderr/exit
ExecSvc -> API: result
API -> DB: INSERT execution_logs
API -> Frontend: result JSON
Frontend -> User: render output below cells
```

### Import `.cppnb`
```
User -> Frontend: Upload file
Frontend -> API: POST /api/notebooks/import (multipart)
API: Parse JSON, create notebook + cells
API -> DB: INSERT notebook, cells
API -> Frontend: { notebook_id }
Frontend: Load notebook view
```

---

## 10) Deployment Topology

- **Containers**
  - `frontend` (Next.js)
  - `api` (FastAPI, uvicorn)
  - `exec` (Execution Microservice)
  - `sqlite` (optional container, or mount local file volume)

- **Networking**
  - Internal docker network: `api` <-> `exec`.
  - External: expose `frontend` only; `frontend` talks to `api` via reverse proxy.

- **Appwrite Deployment**
  - Build multi-service with `docker-compose` for local dev.
  - Provide Dockerfiles and a deploy script for Appwrite platform.

---

## 11) Observability
- **Structured Logging**: request IDs propagated Frontend → API → ExecSvc.
- **Metrics**: count executions, avg duration, error/timeout rates.
- **Health Probes**: `/health` on API and ExecSvc.

---

## 12) Configuration & Limits (initial)
- Max cells per notebook: 100
- Max file size per cell: 200 KB
- Max combined compile size per run: 1.5 MB
- Timeouts: 5s compile + 5s run (hard 10s)
- CPU: 0.5 cores; Memory: 256 MB per execution

---

## 13) Security Hardening (next steps)
- Drop capabilities in Docker (`--cap-drop ALL`).
- Use seccomp/apparmor profiles.
- Read-only root in containers; write only to mounted `/work`.
- Non-root user inside compiler image.

---

## 14) Stretch Design
- Real-time collaboration via WebSocket channel (room = notebook_id).
- AI assistant microservice: explain errors, suggest fixes (OpenAI API).
- Version history using append-only `cell_versions` table.
- Support custom compiler flags per notebook and per run.

---

## 15) Milestone Plan

**Milestone 1 — Core Execution Path (API ↔ ExecSvc)**
- ExecSvc: implement `/run` with Docker; return results.
- API: implement `/api/execute` and minimal validation.
- Manual cURL tests.

**Milestone 2 — Notebook CRUD**
- DB schema, notebook + cell endpoints.
- Export/import `.cppnb`.

**Milestone 3 — Frontend MVP**
- Notebook page, cells UI, Monaco, Run Selected/All.
- Display outputs.

**Milestone 4 — Hardening & Polish**
- Limits, error UX, logs, basic auth (optional).

**Milestone 5 — Stretch (time permitting)**
- AI error helper, sharing, real-time collab.

---

## 16) Open Questions / Choices
- Auth: local (email/password) vs. no-auth for hackathon demo.
- DB: SQLite file volume vs. Postgres (managed) if needed.
- Compiler image: `gcc:latest` vs. `clang:latest` (can support both).
- API ↔ ExecSvc protocol: REST (JSON) now; gRPC later if needed.

---

## 17) Sample Docker Commands

**Compile & run inside sandbox:**
```
docker run --rm \
  --network=none \
  --cpus=0.5 --memory=256m --pids-limit=128 \
  -v /tmp/job-123:/work -w /work \
  gcc:13 \
  bash -lc "g++ -std=c++17 -O2 *.cpp -o program && ./program < input.txt"
```

---

## 18) Acceptance Criteria (Demo)
- Create notebook, add 3 cells (`.h`, `.cpp`, `main.cpp`).
- Run single cell (header: reject; source without `main`: compile-only message).
- Run selected → prints expected output.
- Export `.cppnb`, import back → cells restored identically.
- Sandbox limits enforced (busy loop → timeout message).

---

*End of document.*

