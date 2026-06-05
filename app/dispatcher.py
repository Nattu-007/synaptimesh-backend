from app.commands import ACTION_MAP

DEFAULT_THRESHOLD = 0.70


def dispatch_command(command, confidence=None):

    # Support validated payload dictionaries
    if isinstance(command, dict):
        payload = command
        command = payload.get("command")
        confidence = payload.get("confidence", 1.0)

    # Support direct string commands
    if confidence is None:
        confidence = 1.0

    if confidence < DEFAULT_THRESHOLD:
        return {
            "status": "skipped",
            "message": (
                f"Confidence {confidence:.2f} "
                f"below threshold {DEFAULT_THRESHOLD:.2f}"
            )
        }

    action = ACTION_MAP.get(command)

    if action is None:
        return {
            "status": "error",
            "message": f"Unknown command: {command}"
        }

    try:
        action()

        return {
            "status": "ok",
            "message": f"{command} executed successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }