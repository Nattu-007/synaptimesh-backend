# app/chatbot.py
# Synaptimesh AI Chatbot — powered by Groq (free tier, no credit card needed)
#
# Setup:
#   1. pip install groq
#   2. Get free API key at https://console.groq.com
#   3. Add GROQ_API_KEY=your_key to .env
#
# Exposes:
#   POST /chat/message   — single-turn Q&A
#   POST /chat/session   — multi-turn conversation with history
#   GET  /chat/commands  — list all available EEG commands

import os
from groq import AsyncGroq
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.logger         import get_logger
from app.command_loader import get_action_map, get_eeg_to_action_map
from app.config         import GROQ_API_KEY, GROQ_MODEL, CONFIDENCE_THRESHOLD
from app.webapps.intent_router import detect_intent
from app.webapps.youtube import (
    search_videos,
    play_video
)
from app.webapps.gmail import open_gmail
from app.webapps.netflix import open_netflix

logger = get_logger(__name__)
router = APIRouter()

# ── Groq client (module-level singleton) ──────────────────────────────────────
# AsyncGroq reads GROQ_API_KEY from env automatically, but we pass it
# explicitly so the missing-key error is caught early and clearly.
_groq_client: AsyncGroq | None = None

def get_groq_client() -> AsyncGroq | None:
    global _groq_client
    if not GROQ_API_KEY:
        return None
    if _groq_client is None:
        _groq_client = AsyncGroq(api_key=GROQ_API_KEY)
    return _groq_client

def detect_local_intent(message):

    text = message.lower()

    if "open gmail" in text:
        return ("OPEN_GMAIL", None)

    if "open netflix" in text:
        return ("OPEN_NETFLIX", None)

    if "open youtube" in text:
        return ("OPEN_YOUTUBE", None)

    if text.startswith("play "):
        return (
            "PLAY_YOUTUBE",
            text.replace("play ", "")
        )

    return None

# ── System prompt — gives the model full Synaptimesh context ──────────────────

def build_system_prompt() -> str:
    action_map    = get_action_map()
    eeg_to_action = get_eeg_to_action_map()

    command_list = "\n".join(
        f"  - {cmd}: {meta.get('description', 'No description')}"
        for cmd, meta in action_map.items()
    )

    eeg_map = "\n".join(
        f"  - EEG signal '{eeg}' + category '{cat}' → {action}"
        for (eeg, cat), action in eeg_to_action.items()
    )

    return f"""You are the Synaptimesh AI Assistant — an intelligent support chatbot \
embedded in the Synaptimesh EEG-to-desktop automation backend.

Synaptimesh is a Python FastAPI backend that receives EEG command payloads from \
an Emotiv EPOC X headset, validates them, publishes them to an MQTT broker, and \
executes desktop automation via pyautogui.

CONFIDENCE THRESHOLD: {CONFIDENCE_THRESHOLD}
Any command with confidence below this value is rejected.

AVAILABLE DESKTOP COMMANDS:
{command_list}

EEG SIGNAL → DESKTOP ACTION MAPPINGS:
{eeg_map}

Your role:
- Answer questions about Synaptimesh commands, EEG signals, and system architecture.
- Help users understand why a command failed (low confidence, unknown command, MQTT error, etc.).
- Explain what each EEG signal + category combination maps to.
- Guide users on sending commands via POST /receive-command or the MQTT publisher.
- Be concise, technical, and helpful.
- If asked to "run" or "execute" a command, clarify that you cannot do that directly — \
  the user should use POST /receive-command or python -m app.mqtt_publisher.

Respond in plain text. Be concise but thorough."""


# ── Request / Response schemas ────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role:    str    # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str

class SessionRequest(BaseModel):
    message: str
    history: Optional[list[ChatMessage]] = []


# ── Groq API helper ───────────────────────────────────────────────────────────

async def call_groq(messages: list[dict], system: str) -> str:
    """
    Sends messages to Groq and returns the assistant reply as a string.
    Groq uses OpenAI-compatible chat completions format.
    System prompt is injected as the first message with role="system".
    """
    client = get_groq_client()
    if client is None:
        logger.warning("GROQ_API_KEY not set — chatbot unavailable.")
        return (
            "Chatbot is not configured. "
            "Set GROQ_API_KEY in your .env file and restart the server.\n"
            "Get a free key at: https://console.groq.com"
        )

    # Groq uses the same format as OpenAI:
    # system prompt goes in as the first message with role="system"
    full_messages = [{"role": "system", "content": system}] + messages

    try:
        response = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=full_messages,
            max_tokens=1024,
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        logger.debug(
            f"Groq response | model={GROQ_MODEL} "
            f"| input_tokens={response.usage.prompt_tokens} "
            f"| output_tokens={response.usage.completion_tokens}"
        )
        return reply

    except Exception as e:
        logger.error(f"Groq API call failed: {e}", exc_info=True)
        return f"Chatbot error: {str(e)}"


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/message")
async def chat_message(req: ChatRequest):
    """
    Single-turn chat — no history needed.

    POST /chat/message
    Body: { "message": "What does LEFT_HAND do in media mode?" }

    PowerShell:
    Invoke-RestMethod -Uri http://127.0.0.1:5000/chat/message `
      -Method POST -ContentType "application/json" `
      -Body '{"message": "What is the confidence threshold?"}'
    """
    logger.info(f"Chat message: {req.message[:80]}")
    system = build_system_prompt()
    reply  = await call_groq(
        messages=[{"role": "user", "content": req.message}],
        system=system,
    )
    return {"reply": reply}


@router.post("/session")
async def chat_session(req: SessionRequest):
    """
    Multi-turn chat — pass conversation history to maintain context.

    POST /chat/session
    Body:
    {
      "message": "Why was my PLAY command rejected?",
      "history": [
        {"role": "user",      "content": "What is the threshold?"},
        {"role": "assistant", "content": "The threshold is 0.70..."}
      ]
    }

    The response includes an updated "history" array — pass it back
    in the next request to continue the conversation.
    """
    logger.info(f"Chat session message: {req.message[:80]}")
    system = build_system_prompt()

    messages = [{"role": m.role, "content": m.content} for m in (req.history or [])]
    messages.append({"role": "user", "content": req.message})

    reply = await call_groq(messages=messages, system=system)

    return {
        "reply":   reply,
        "history": messages + [{"role": "assistant", "content": reply}],
    }


@router.get("/commands")
async def list_commands():
    """
    Returns all verified EEG commands with metadata.
    Useful for building a command reference UI or debugging.

    GET /chat/commands
    """
    action_map = get_action_map()
    return {
        "total":    len(action_map),
        "model":    GROQ_MODEL,
        "commands": [
            {
                "command":     cmd,
                "category":    meta.get("category", "unknown"),
                "eeg_signal":  meta.get("command", "unknown"),
                "description": meta.get("description", ""),
                "confidence":  meta.get("confidence", 0.0),
            }
            for cmd, meta in action_map.items()
        ],
    }


@router.get("/status")
async def chatbot_status():
    """
    Returns chatbot configuration status.
    Useful for health checks and debugging setup issues.

    GET /chat/status
    """
    configured = bool(GROQ_API_KEY)
    return {
        "configured": configured,
        "model":      GROQ_MODEL if configured else None,
        "provider":   "Groq",
        "free_tier":  True,
        "signup_url": "https://console.groq.com",
        "status":     "ready" if configured else "missing GROQ_API_KEY in .env",
    }
