# app/dispatcher.py
# Routes validated commands to desktop automation functions
# Adds structured logging and proper exception wrapping

from app.commands import ACTION_MAP
from app.config   import CONFIDENCE_THRESHOLD
from app.logger   import get_logger
from app.exceptions import (
    ConfidenceTooLowError,
    UnknownCommandError,
    AutomationError,
)

logger = get_logger(__name__)


def dispatch_command(command, confidence=None) -> dict:
    """
    Dispatch a command to the appropriate pyautogui action.

    Accepts:
      - dict  (validated payload from /receive-command)
      - str   (direct command name)

    Returns:
        dict with status, message, and command name

    Raises:
        ConfidenceTooLowError, UnknownCommandError, AutomationError
    """

    # ── Normalise input ────────────────────────────────
    if isinstance(command, dict):
        payload    = command
        command    = payload.get("command")
        confidence = payload.get("confidence", 1.0)

    if confidence is None:
        confidence = 1.0

    logger.info(f"Dispatch requested | command={command} | confidence={confidence:.2f}")

    # ── Confidence gate ────────────────────────────────
    if confidence < CONFIDENCE_THRESHOLD:
        logger.warning(
            f"Skipped '{command}' — confidence {confidence:.2f} "
            f"< threshold {CONFIDENCE_THRESHOLD:.2f}"
        )
        raise ConfidenceTooLowError(confidence, CONFIDENCE_THRESHOLD)

    # ── Command lookup ─────────────────────────────────
    action = ACTION_MAP.get(command)
    if action is None:
        logger.error(f"Unknown command: '{command}'")
        raise UnknownCommandError(command)

    # ── Execute ────────────────────────────────────────
    try:
        action()
        logger.info(f"Executed '{command}' successfully")
        return {
            "status":  "ok",
            "message": f"{command} executed successfully",
            "command": command,
        }
    except Exception as e:
        logger.error(f"Automation error for '{command}': {e}", exc_info=True)
        raise AutomationError(command, str(e))
