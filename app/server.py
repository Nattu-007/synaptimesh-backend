# app/server.py
# Synaptimesh FastAPI server — Day 4
# Adds: structured logging, global exception handlers, chatbot route

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.schema     import CommandPayload, validate_command
from app.mqtt_client import publish_command, connect, is_connected
from app.dispatcher import dispatch_command
from app.config     import SERVER_HOST, SERVER_PORT, SERVER_DEBUG
from app.logger     import get_logger
from app.exceptions import (
    SynaptimeshError,
    InvalidPayloadError,
    ConfidenceTooLowError,
    UnknownCommandError,
    AutomationError,
    MQTTConnectionError,
    MQTTNotConnectedError,
)
from app.chatbot import router as chatbot_router
from app.webapps.youtube import (
    search_videos,
    play_video
)

logger = get_logger(__name__)

app = FastAPI(title="SynaptiMesh Backend", version="0.1.0")

# ── Mount chatbot routes ──────────────────────────────────────────────────────
app.include_router(chatbot_router, prefix="/chat", tags=["Chatbot"])


# ── Startup / Shutdown ────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    logger.info("SynaptiMesh backend starting up...")
    try:
        connect()
    except MQTTConnectionError as e:
        logger.error(f"MQTT startup failed: {e} — continuing without MQTT.")


@app.on_event("shutdown")
async def shutdown():
    logger.info("SynaptiMesh backend shutting down.")


# ── Global Exception Handlers ─────────────────────────────────────────────────

HTTP_STATUS_MAP = {
    "INVALID_PAYLOAD":       400,
    "UNKNOWN_COMMAND":       400,
    "LOW_CONFIDENCE":        422,
    "AUTOMATION_ERROR":      500,
    "MQTT_CONNECTION_ERROR": 503,
    "MQTT_PUBLISH_ERROR":    503,
    "MQTT_NOT_CONNECTED":    503,
}

@app.exception_handler(SynaptimeshError)
async def synaptimesh_error_handler(request: Request, exc: SynaptimeshError):
    status = HTTP_STATUS_MAP.get(exc.code, 500)
    logger.warning(f"Handled [{exc.code}]: {exc.message}")
    return JSONResponse(status_code=status, content={
        "error":  exc.code,
        "detail": exc.message,
    })

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={
        "error":  "INTERNAL_ERROR",
        "detail": "An unexpected error occurred.",
    })


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def home():
    return {"service": "SynaptiMesh Backend", "status": "running"}


@app.get("/health")
async def health():
    mqtt_status = "connected" if is_connected() else "disconnected"
    logger.debug(f"Health check — MQTT: {mqtt_status}")
    return {
        "status":  "healthy",
        "service": "SynaptiMesh Backend",
        "mqtt":    mqtt_status,
    }


@app.post("/receive-command")
async def receive_command(payload: CommandPayload):
    validated, error = validate_command(payload.dict())
    if error:
        logger.warning(f"Payload validation failed: {error}")
        raise InvalidPayloadError(error)

    logger.info(f"Received command: {validated.get('command')} | conf={validated.get('confidence')}")

    # Publish to MQTT (non-fatal if broker is down)
    try:
        publish_command(validated)
    except (MQTTNotConnectedError, MQTTConnectionError) as e:
        logger.warning(f"MQTT publish skipped: {e}")

    # Execute desktop automation
    result = dispatch_command(validated)

    return {"status": "ok", "command": validated, "dispatch": result}

@app.get("/youtube/search")
async def youtube_search(query: str):

    return search_videos(query)

@app.get("/youtube/play")
async def youtube_play(query: str):

    return play_video(query)

# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info(f"Starting uvicorn on {SERVER_HOST}:{SERVER_PORT} | debug={SERVER_DEBUG}")
    uvicorn.run(
        "app.server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_DEBUG,
    )
