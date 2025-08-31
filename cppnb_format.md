# 📑 `.cppnb` File Format Specification

The **`.cppnb`** file format is a JSON-based structure used by the **C++ Notebook** project.
It defines how notebooks, cells, outputs, and execution groups are stored and restored.

---

## 📂 File Details

- **Extension:** `.cppnb`
- **Format:** JSON
- **Purpose:** Store notebook code, metadata, outputs, and execution history.

---

## 🔹 Top-Level Structure

```json
{
  "notebook_name": "My First Notebook",
  "created_at": "2025-08-28T12:00:00Z",
  "updated_at": "2025-08-28T12:30:00Z",
  "metadata": {
    "author": "Ayush Goyal",
    "language": "C++17",
    "description": "Experimenting with classes and functions."
  },
  "cells": [ ... ],
  "execution_groups": [ ... ]
}
📝 Fields Explanation
Notebook Metadata
notebook_name → Human-readable notebook title.

created_at / updated_at → ISO timestamps for tracking creation & edits.

metadata → Freeform metadata:

author: Notebook creator.

language: C++ standard used (e.g., C++11, C++17).

description: Optional notes or summary.

Cells
Each cell maps to a C++ file (.cpp or .h).

json
Copy code
{
  "id": "cell-1",
  "type": "source",
  "filename": "main.cpp",
  "code": "#include <iostream>\nint main(){ std::cout << \"Hello\"; }",
  "outputs": []
}
id → Unique cell identifier.

type → "source" (for .cpp) or "header" (for .h).

filename → Suggested filename when writing files before compilation.

code → Raw C++ code.

outputs → List of past execution results for this cell.

Outputs
Each execution result is logged:

json
Copy code
{
  "stdout": "Hello\n",
  "stderr": "",
  "exit_code": 0,
  "status": "success",
  "timestamp": "2025-08-28T12:05:00Z"
}
stdout → Standard output.

stderr → Error output.

exit_code → Compiler/runtime exit code.

status → "success" | "compile_error" | "runtime_error" | "timeout".

timestamp → When the run occurred.

Execution Groups
Optional feature: users can define bundles of cells to run together.

json
Copy code
{
  "id": "group-1",
  "name": "Main with Utils",
  "cell_ids": ["cell-1", "cell-2", "cell-3"],
  "last_run": "2025-08-28T12:20:00Z",
  "outputs": {
    "stdout": "Hello\n",
    "stderr": "",
    "exit_code": 0,
    "status": "success"
  }
}
id → Unique group identifier.

name → Friendly group name.

cell_ids → Array of cell references.

last_run → Last execution timestamp.

outputs → Combined result of the group execution.

🔄 Example Workflow
Save → Notebook is serialized to .cppnb.

Upload → Parsing .cppnb restores all cells and outputs in frontend.

Execute → Backend compiles referenced cells (g++ file1.cpp file2.cpp -o program).

Reuse → Users can run saved execution groups without re-selecting cells.

✅ Benefits of .cppnb Format
Faithful to Jupyter model → Cells + outputs.

Extensible → Can add AI hints, debug metadata, or collaboration info later.

Multi-file ready → Natural handling of .cpp + .h files.

Portable & simple → JSON is easy to parse in both frontend & backend.

📂 Minimal Example
json
Copy code
{
  "notebook_name": "Hello World",
  "created_at": "2025-08-31T10:00:00Z",
  "updated_at": "2025-08-31T10:05:00Z",
  "metadata": {
    "author": "Student",
    "language": "C++17",
    "description": "Basic hello world example."
  },
  "cells": [
    {
      "id": "cell-1",
      "type": "source",
      "filename": "main.cpp",
      "code": "#include <iostream>\nint main(){ std::cout << \"Hello World\"; }",
      "outputs": [
        {
          "stdout": "Hello World\n",
          "stderr": "",
          "exit_code": 0,
          "status": "success",
          "timestamp": "2025-08-31T10:05:00Z"
        }
      ]
    }
  ]
}
