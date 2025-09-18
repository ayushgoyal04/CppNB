
# logic.py
from __future__ import annotations
from typing import Optional, List
from datetime import datetime
import tempfile
import subprocess
import uuid
import os
import json

from database import NotebookRepo, Notebook, Cell

# ---------------------------
# 🗒 Notebook Management (business logic)
# ---------------------------

def new_notebook() -> Notebook:
    nb = Notebook(
        metadata={
            "name": "Untitled Notebook",
            "version": "1.0",
            "language": "cpp",
            "created": datetime.utcnow().isoformat(),
            "modified": datetime.utcnow().isoformat(),
        },
        cells=[Cell(id=1, code="// New cell")],
    )
    NotebookRepo.set(nb)
    return nb


def save_notebook_logic(notebook: Notebook):
    notebook.metadata["modified"] = datetime.utcnow().isoformat()
    NotebookRepo.set(notebook)
    return {"status": "saved", "notebook": notebook}


def load_notebook_logic() -> Optional[Notebook]:
    return NotebookRepo.get()


def upload_notebook_logic(raw_bytes: bytes):
    try:
        data = json.loads(raw_bytes.decode())
        nb = Notebook(**data)
    except Exception as e:
        raise ValueError(f"Invalid notebook format: {e}")
    NotebookRepo.set(nb)
    return {"status": "uploaded", "notebook": nb}


def download_notebook_logic() -> Optional[str]:
    nb = NotebookRepo.get()
    if not nb:
        return None
    tmp_path = f"/tmp/{uuid.uuid4()}.cppnb.json"
    with open(tmp_path, "w") as f:
        f.write(nb.json(indent=2))
    return tmp_path

