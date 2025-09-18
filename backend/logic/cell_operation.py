
# ---------------------------
# 📝 Cell Operations
# ---------------------------

def _ensure_notebook() -> Notebook:
    nb = NotebookRepo.get()
    if not nb:
        raise KeyError("No notebook loaded")
    return nb


def add_cell_logic(after_id: Optional[int] = None) -> Optional[Notebook]:
    nb = NotebookRepo.get()
    if not nb:
        return None
    new_id = max((cell.id for cell in nb.cells), default=0) + 1
    new_cell = Cell(id=new_id, code="// New cell")
    if after_id is not None:
        idx = next((i for i, c in enumerate(nb.cells) if c.id == after_id), None)
        if idx is not None:
            nb.cells.insert(idx + 1, new_cell)
        else:
            nb.cells.append(new_cell)
    else:
        nb.cells.append(new_cell)
    NotebookRepo.set(nb)
    return nb


def delete_cell_logic(cell_id: int) -> Optional[Notebook]:
    nb = NotebookRepo.get()
    if not nb:
        return None
    nb.cells = [c for c in nb.cells if c.id != cell_id]
    NotebookRepo.set(nb)
    return nb


def update_cell_logic(cell_id: int, cell: Cell):
    nb = NotebookRepo.get()
    if not nb:
        return None
    for i, c in enumerate(nb.cells):
        if c.id == cell_id:
            nb.cells[i] = cell
            NotebookRepo.set(nb)
            return nb
    return False  # cell not found

