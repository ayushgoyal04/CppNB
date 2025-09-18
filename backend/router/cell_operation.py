
# ---------------------------
# 📝 Cell Operations
# ---------------------------

@router.post("/cell/add")
def cell_add(after_id: Optional[int] = None):
    nb = add_cell_logic(after_id)
    if not nb:
        raise HTTPException(status_code=404, detail="No notebook loaded")
    return nb

@router.delete("/cell/{cell_id}")
def cell_delete(cell_id: int):
    nb = delete_cell_logic(cell_id)
    if not nb:
        raise HTTPException(status_code=404, detail="No notebook loaded")
    return nb

@router.put("/cell/{cell_id}")
def cell_update(cell_id: int, cell: Cell):
    nb = update_cell_logic(cell_id, cell)
    if not nb:
        raise HTTPException(status_code=404, detail="No notebook loaded")
    if nb is False:
        raise HTTPException(status_code=404, detail="Cell not found")
    return nb
