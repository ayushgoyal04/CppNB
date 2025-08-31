from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RunRequest(BaseModel):
    code: str

@app.post("/run")
def run_code(req: RunRequest):
    # For now, just echo back (later add Docker sandbox)
    return {
        "stdout": req.code,
        "stderr": "",
        "exit_code": 0
    }

@app.get("/health")
def health():
    return {"status": "exec alive"}
