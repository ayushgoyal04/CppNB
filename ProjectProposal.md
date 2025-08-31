# 📘 C++ Notebook – Interactive Multi-Cell C++ Playground

An interactive notebook-style environment for **C++**, inspired by Jupyter Notebook but designed specifically for C++ learners, educators, and developers.
This project provides a **sandboxed, web-based playground** where users can create, run, and share multi-file C++ projects in a notebook-style interface.

---

## 🚩 Problem Statement

C++ is one of the most widely used programming languages in systems programming, embedded systems, and competitive programming.
However, its learning and experimentation experience lags behind modern interactive environments like Jupyter Notebook for Python.

**Current pain points:**
- ❌ No interactive, notebook-style environment for C++ experimentation.
- ❌ Complicated setup (IDEs, compilers, dependencies).
- ❌ Hard to work incrementally with multi-file projects.
- ❌ Lack of safe, sandboxed environments for running untrusted C++ code online.

---

## 💡 Proposed Solution

I aim to build a **C++ Notebook Web Application** hosted on Appwrite’s deployment platform.

**Key Features:**
- Notebook interface with cells (`.cpp` or `.h` files).
- Run single or multiple cells (multi-file compilation supported).
- Sandboxed execution inside Docker for safety.
- Custom `.cppnb` file format for saving/loading notebooks.
- Export notebooks to `.cpp` files for external use.
- Minimal and intuitive UI with syntax highlighting.

---

## 🎯 Objectives

- Provide a **web-based IDE-like experience** for C++.
- Ensure **secure, sandboxed compilation** inside containers.
- Support **multi-file project execution**.
- Enable **persistence of notebooks** with import/export.
- Deliver a **hackathon-ready product** showcasing strong backend engineering.

---

## 👥 Target Users

- **Students & Educators** – teaching and learning C++.
- **Competitive Programmers** – quickly test snippets in a notebook style.
- **Developers** – experiment with algorithms and multi-file projects.

---

## ✅ Features

### Core (MVP)
- **Notebook Management** – Create, save, load, delete notebooks.
- **Cells** – Add, remove, reorder cells with `.cpp` or `.h` type.
- **Execution** – Compile & run inside Docker sandbox with error/output handling.
- **Custom File Format** – `.cppnb` (JSON-based, stores cells, code, outputs, metadata).

### 🚀 Stretch Goals
- Real-time collaboration.
- AI-powered error explanations & code suggestions.
- Version history for notebooks.
- Export to `.pdf` / `.md`.
- Snippet/template library for C++ patterns.

---

## 🛠️ Tech Stack

### Frontend
- **Next.js (React)** – framework.
- **Monaco Editor** – in-browser code editor.
- **TailwindCSS + shadcn/ui** – styling & UI.

### Backend API
- **FastAPI (Python)** – REST API service.
- Handles Notebook CRUD, `.cppnb` parsing, and execution orchestration.

### Execution Microservice
- **Dockerized g++ runner** – compiles & runs code in isolation.
- Resource limits for CPU, memory, and runtime.

### Database & Storage
- **SQLite** – lightweight DB for hackathon.
- `.cppnb` files stored as JSON blobs.

### Deployment
- **Docker Compose** – multi-service orchestration.
- Deployed via **Appwrite Deployment Service**.

---

## 🏗️ Architecture

**High-Level Flow:**
1. User edits notebook in frontend.
2. API service handles save/load/execute requests.
3. Execution microservice runs code in sandboxed Docker containers.
4. Output/errors returned → displayed in frontend cells.

**Components:**
- Frontend (Next.js)
- Backend API (FastAPI)
- Execution Microservice (Docker sandbox)
- Database (SQLite)

---

## 🔒 Security Considerations

- Execution runs in isolated **Docker containers**.
- Strict **CPU, memory, runtime limits**.
- **No network access** inside containers.
- Automatic cleanup after execution.

---

## 🚀 Deployment Plan

- Containerize each service (frontend, backend, execution, DB).
- Orchestrate with `docker-compose.yml`.
- Deploy to **Appwrite** platform.
- Expose frontend as main entry point.

---

## 🎉 Expected Outcomes

- A working **interactive C++ notebook system**.
- Judges see:
  - Innovative idea (C++ Jupyter equivalent).
  - Strong backend & sandbox security.
  - Clean, minimal UI.
- A **scalable foundation** for future features like AI helpers & collaboration.

---

## 📂 Example `.cppnb` File (JSON)

```json
{
  "metadata": { "title": "Hello World Notebook", "created_at": "2025-08-31" },
  "cells": [
    { "type": "cpp", "code": "#include <iostream>\nint main(){ std::cout << \"Hello, World!\"; }", "output": "Hello, World!" },
    { "type": "h", "code": "#pragma once\nvoid greet();" }
  ]
}
