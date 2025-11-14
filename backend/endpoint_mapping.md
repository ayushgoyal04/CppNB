Backend API Endpoints + CppNB Document Format
1. Base Setup

Framework: FastAPI

Execution: Sandbox for C++ (compile + run with resource limits)

Storage: In-memory (later per-user DB)

Notebook Format: .cppnb.json (JSON-based custom format)

2. CppNB Document Format

Each notebook file (.cppnb.json) will be JSON with the following schema:

{
  "metadata": {
    "name": "CppNB Notebook",
    "version": "1.0",
    "language": "cpp",
    "created": "2025-09-01T12:00:00Z",
    "modified": "2025-09-01T12:15:00Z"
  },
  "cells": [
    {
      "id": 1,
      "type": "code",
      "code": "#include <iostream>\nint main() { std::cout << 42; }",
      "output": "",
      "selected": false
    },
    {
      "id": 2,
      "type": "code",
      "code": "int x = 10; std::cout << x * 2;",
      "output": "",
      "selected": true
    }
  ]
}

🔹 Rules

metadata: notebook-level info (name, version, language).

cells: array of objects.

id: unique identifier for the cell.

type: "code" (future: "markdown", "text").

code: raw C++ source code for that cell.

output: last execution result (string).

selected: whether the cell is currently selected in UI.

3. Endpoints
🔹 Notebook Management

POST /notebook/new → return fresh notebook with 1 empty cell.

POST /notebook/save → accept notebook JSON, store in memory, return success.

GET /notebook/load → return current notebook JSON.

POST /notebook/upload

Accepts file upload (.cppnb.json).

Parse JSON, validate schema.

Return parsed notebook.

GET /notebook/download

Return current notebook as downloadable .cppnb.json file.

🔹 Cell Operations

POST /cell/add → add new cell after given id.

DELETE /cell/{id} → remove cell.

PUT /cell/{id} → update cell code.

🔹 Execution

POST /run/cell/{id} → compile + run that cell’s code, return output.

POST /run/selected → run all selected cells in sequence, return outputs.

4. Execution Sandbox

Compile with g++ -std=c++17 temp.cpp -o temp.out.

Run with subprocess (timeout & memory limit).

Capture stdout + stderr.

Return output string to frontend.

5. Future Extensions

Multiple languages (language in metadata).

Markdown / text cells.

User-based storage (DB + auth).

Versioning system.
