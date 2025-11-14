
# ---------------------------
# ⚡ Execution
# ---------------------------

@router.post("/run/cell/{cell_id}")
def run_cell(cell_id: int):
    try:
        return run_cell_logic(cell_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="No notebook loaded")
    except ValueError:
        raise HTTPException(status_code=404, detail="Cell not found")

@router.post("/run/selected")
def run_selected():
    try:
        return run_selected_logic()
    except KeyError:
        raise HTTPException(status_code=404, detail="No notebook loaded")


# App bootstrap kept minimal, so `uvicorn router:app --reload` works directly.
app = FastAPI(title="CppNB Backend", version="1.0")
app.include_router(router)

