# app/server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from app.schema import CommandPayload, validate_command
from app.mqtt_client import publish_command
from app.dispatcher import dispatch_command
from app.config import SERVER_HOST, SERVER_PORT, SERVER_DEBUG

load_dotenv()

app = FastAPI(title="SynaptiMesh Backend", version="0.1.0")

@app.post("/receive-command")
async def receive_command(payload: CommandPayload):
    # Step 1: Validate
    validated, error = validate_command(payload.dict())
    if error:
        raise HTTPException(status_code=400, detail=error)

    # Step 2: Publish to MQTT (broadcasts to IoT & Embedded teams)
    publish_command(validated)

    # Step 3: Execute desktop automation
    result = dispatch_command(validated)

    return {
        "status": "ok",
        "command": validated,
        "dispatch": result
    }

@app.get("/")
async def home():
    return {
        "service": "SynaptiMesh Backend",
        "status":  "running"
    }

@app.get("/health")
async def health():
    return {
        "status":  "healthy",
        "service": "SynaptiMesh Backend",
        "mqtt":    "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_DEBUG
    )