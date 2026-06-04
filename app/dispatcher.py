# app/dispatcher.py
from app.commands import execute_command, ACTION_MAP
from app.config import CONFIDENCE_THRESHOLD

COMMAND_REGISTRY = set(ACTION_MAP.keys())

def dispatch_command(validated: dict) -> dict:
    """
    Receives an already-validated payload dict.
    Applies confidence gating, then executes desktop automation.
    """
    command    = validated.get("command")
    confidence = validated.get("confidence", 0.0)

    # Check registry
    if command not in COMMAND_REGISTRY:
        return {"status": "error", "message": f"Unknown command: {command}"}

    # Confidence gate
    if confidence < CONFIDENCE_THRESHOLD:
        return {
            "status": "skipped",
            "message": f"Confidence {confidence:.2f} below threshold {CONFIDENCE_THRESHOLD}"
        }

    # Execute
    result = execute_command(command)
    return {"status": "ok", "command": command, "result": result}