# app/dispatcher.py

from app.commands import ACTION_MAP
from app.config import CONFIDENCE_THRESHOLD
from app.logger import get_logger

from app.exceptions import (
    ConfidenceTooLowError,
    UnknownCommandError,
    AutomationError,
)

# Optional web-app actions
try:
    from app.webapps.gmail import open_gmail
    from app.webapps.netflix import open_netflix
    from app.webapps.youtube import (
        open_youtube,
        play_video
    )
except ImportError:
    open_gmail = None
    open_netflix = None
    open_youtube = None
    play_video = None


logger = get_logger(__name__)


WEBAPP_ACTIONS = {
    "OPEN_GMAIL": open_gmail,
    "OPEN_NETFLIX": open_netflix,
    "OPEN_YOUTUBE": open_youtube,
}


def dispatch_command(command, confidence=None) -> dict:
    """
    Dispatch command to desktop automation,
    chatbot actions, or web applications.
    """

    # --------------------------------------
    # Normalise input
    # --------------------------------------

    youtube_query = None

    if isinstance(command, dict):

        payload = command

        command = payload.get("command")

        confidence = payload.get(
            "confidence",
            1.0
        )

        youtube_query = payload.get(
            "query"
        )

    if confidence is None:
        confidence = 1.0

    logger.info(
        f"Dispatch requested | "
        f"command={command} | "
        f"confidence={confidence:.2f}"
    )

    # --------------------------------------
    # Confidence Gate
    # --------------------------------------

    if confidence < CONFIDENCE_THRESHOLD:

        logger.warning(
            f"Skipped '{command}' "
            f"confidence={confidence:.2f} "
            f"< threshold={CONFIDENCE_THRESHOLD:.2f}"
        )

        raise ConfidenceTooLowError(
            confidence,
            CONFIDENCE_THRESHOLD
        )

    # --------------------------------------
    # Dynamic YouTube Command
    # --------------------------------------

    if command == "PLAY_YOUTUBE_VIDEO":

        if play_video is None:

            raise AutomationError(
                command,
                "YouTube module not installed"
            )

        try:

            result = play_video(
                youtube_query
            )

            logger.info(
                f"YouTube playback started "
                f"for query='{youtube_query}'"
            )

            return {
                "status": "ok",
                "command": command,
                "query": youtube_query,
                "video": result
            }

        except Exception as e:

            logger.error(
                f"YouTube playback failed: {e}",
                exc_info=True
            )

            raise AutomationError(
                command,
                str(e)
            )

    # --------------------------------------
    # Web App Actions
    # --------------------------------------

    if command in WEBAPP_ACTIONS:

        action = WEBAPP_ACTIONS.get(command)

        if action is None:

            raise AutomationError(
                command,
                "Action not available"
            )

        try:

            action()

            logger.info(
                f"Web app command executed: "
                f"{command}"
            )

            return {
                "status": "ok",
                "message":
                f"{command} executed successfully",
                "command": command
            }

        except Exception as e:

            logger.error(
                f"Web app execution failed "
                f"for {command}: {e}",
                exc_info=True
            )

            raise AutomationError(
                command,
                str(e)
            )

    # --------------------------------------
    # Existing Desktop Commands
    # --------------------------------------

    action = ACTION_MAP.get(command)

    if action is None:

        logger.error(
            f"Unknown command: '{command}'"
        )

        raise UnknownCommandError(
            command
        )

    try:

        action()

        logger.info(
            f"Executed '{command}' successfully"
        )

        return {
            "status": "ok",
            "message":
            f"{command} executed successfully",
            "command": command
        }

    except Exception as e:

        logger.error(
            f"Automation error "
            f"for '{command}': {e}",
            exc_info=True
        )

        raise AutomationError(
            command,
            str(e)
        )