from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "backend alive"}

@app.post("/execute")
async def execute_code(code: str):
    # Forward request to exec service
    async with httpx.AsyncClient() as client:
        resp = await client.post("http://exec:9000/run", json={"code": code})
        return resp.json()
