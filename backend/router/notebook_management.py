# router.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.routing import APIRouter
from typing import Optional
from datetime import datetime

from logic import (
    new_notebook,
    save_notebook_logic,
    load_notebook_logic,
    upload_notebook_logic,
    download_notebook_logic,
    add_cell_logic,
    delete_cell_logic,
    update_cell_logic,
    run_cell_logic,
    run_selected_logic,
)
from database import Notebook, Cell

router = APIRouter()

# ---------------------------
# 🗒 Notebook Management
# ---------------------------

@router.post("/notebook/new")
def notebook_new():
    return new_notebook()

@router.post("/notebook/save")
def notebook_save(notebook: Notebook):
    return save_notebook_logic(notebook)

@router.get("/notebook/load")
def notebook_load():
    nb = load_notebook_logic()
    if not nb:
        raise HTTPException(status_code=404, detail="No notebook found")
    return nb

@router.post("/notebook/upload")
async def notebook_upload(file: UploadFile = File(...)):
    content = await file.read()
    try:
        return upload_notebook_logic(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/notebook/download")
def notebook_download():
    path = download_notebook_logic()
    if not path:
        raise HTTPException(status_code=404, detail="No notebook to download")
    return FileResponse(path, filename="notebook.cppnb.json", media_type="application/json")
