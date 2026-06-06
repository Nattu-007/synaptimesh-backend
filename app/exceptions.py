# app/exceptions.py
# Custom exception hierarchy for Synaptimesh — used across all three layers


class SynaptimeshError(Exception):
    """Base class for all Synaptimesh exceptions."""
    def __init__(self, message: str, code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.code    = code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code}] {self.message}"


# ── Server / Validation Layer ─────────────────────────────────────────────────

class InvalidPayloadError(SynaptimeshError):
    def __init__(self, detail: str = "Malformed or missing payload fields."):
        super().__init__(detail, code="INVALID_PAYLOAD")

class UnknownCommandError(SynaptimeshError):
    def __init__(self, command: str):
        super().__init__(f"Unknown command: '{command}'", code="UNKNOWN_COMMAND")

class ConfidenceTooLowError(SynaptimeshError):
    def __init__(self, confidence: float, threshold: float):
        super().__init__(
            f"Confidence {confidence:.2f} below threshold {threshold:.2f}.",
            code="LOW_CONFIDENCE"
        )


# ── Automation Layer ──────────────────────────────────────────────────────────

class AutomationError(SynaptimeshError):
    def __init__(self, action: str, reason: str = ""):
        msg = f"Automation failed for '{action}'."
        if reason:
            msg += f" Reason: {reason}"
        super().__init__(msg, code="AUTOMATION_ERROR")


# ── MQTT Layer ────────────────────────────────────────────────────────────────

class MQTTConnectionError(SynaptimeshError):
    def __init__(self, broker: str, port: int):
        super().__init__(
            f"Cannot connect to MQTT broker at {broker}:{port}",
            code="MQTT_CONNECTION_ERROR"
        )

class MQTTPublishError(SynaptimeshError):
    def __init__(self, topic: str, reason: str = ""):
        msg = f"Publish failed on topic '{topic}'."
        if reason:
            msg += f" {reason}"
        super().__init__(msg, code="MQTT_PUBLISH_ERROR")

class MQTTNotConnectedError(SynaptimeshError):
    def __init__(self):
        super().__init__(
            "MQTT client is not connected. Call connect() first.",
            code="MQTT_NOT_CONNECTED"
        )
