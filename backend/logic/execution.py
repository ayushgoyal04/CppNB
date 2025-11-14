
# ---------------------------
# ⚡ Execution
# ---------------------------

def _run_cpp_code(code: str) -> str:
    """Compile & run C++ code with basic safeguards (timeouts, temp dirs)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cpp_file = os.path.join(tmpdir, "main.cpp")
        exe_file = os.path.join(tmpdir, "main.out")
        with open(cpp_file, "w") as f:
            f.write(code)
        try:
            compile_proc = subprocess.run(
                ["g++", "-std=c++17", cpp_file, "-o", exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )
            if compile_proc.returncode != 0:
                return f"Compilation Error:\n{compile_proc.stderr}"
            run_proc = subprocess.run(
                [exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5,
            )
            output = (run_proc.stdout or "") + (run_proc.stderr or "")
            return output.strip()
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out"


def run_cell_logic(cell_id: int):
    nb = _ensure_notebook()
    cell = next((c for c in nb.cells if c.id == cell_id), None)
    if not cell:
        raise ValueError("Cell not found")
    output = _run_cpp_code(cell.code)
    cell.output = output
    NotebookRepo.set(nb)
    return {"cell_id": cell_id, "output": output}


def run_selected_logic():
    nb = _ensure_notebook()
    results = []
    for cell in nb.cells:
        if cell.selected:
            output = _run_cpp_code(cell.code)
            cell.output = output
            results.append({"cell_id": cell.id, "output": output})
    NotebookRepo.set(nb)
    return results

