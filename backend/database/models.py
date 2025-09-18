
# database.py
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
import threading

# ---------------------------
# 📄 Models (schemas)
# ---------------------------

class Cell(BaseModel):
    id: int
    type: str = Field("code", regex=r"^(code)$")  # future: markdown, text
    code: str
    output: Optional[str] = ""
    selected: bool = False

class Notebook(BaseModel):
    metadata: dict
    cells: List[Cell]
