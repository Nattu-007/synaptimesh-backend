# tests/test_day4.py
# Synaptimesh Day 4 — Full unit test suite
# Run: pytest tests/test_day4.py -v

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient

from app.server import app
from app.schema import CommandPayload, validate_command
from app.dispatcher import dispatch_command
from app.config import CONFIDENCE_THRESHOLD
from app.exceptions import (
    ConfidenceTooLowError,
    UnknownCommandError,
    InvalidPayloadError,
    AutomationError,
    MQTTPublishError,
    MQTTNotConnectedError,
    MQTTConnectionError,
)

client = TestClient(app)


# ══════════════════════════════════════════════════════════════════
# 1. SCHEMA VALIDATION
# ══════════════════════════════════════════════════════════════════

class TestSchema:

    def test_valid_full_payload(self):
        data, err = validate_command({
            "command": "PLAY", "confidence": 0.92, "source": "EEG"
        })
        assert err is None
        assert data["command"] == "PLAY"

    def test_valid_eeg_signal_payload(self):
        data, err = validate_command({
            "eeg_signal": "LEFT_HAND", "category": "media", "confidence": 0.85
        })
        assert err is None

    def test_missing_command_and_eeg_signal(self):
        data, err = validate_command({"confidence": 0.9})
        assert data is None
        assert err is not None

    def test_confidence_below_zero_rejected(self):
        data, err = validate_command({"command": "PLAY", "confidence": -0.1})
        assert data is None

    def test_confidence_above_one_rejected(self):
        data, err = validate_command({"command": "PLAY", "confidence": 1.5})
        assert data is None

    def test_missing_confidence_rejected(self):
        data, err = validate_command({"command": "PLAY"})
        assert data is None

    def test_source_defaults_to_eeg(self):
        data, err = validate_command({"command": "PAUSE", "confidence": 0.9})
        assert data["source"] == "EEG"

    def test_command_pydantic_model_direct(self):
        p = CommandPayload(command="MUTE", confidence=0.88)
        assert p.command == "MUTE"


# ══════════════════════════════════════════════════════════════════
# 2. DISPATCHER
# ══════════════════════════════════════════════════════════════════

class TestDispatcher:

    @patch("app.dispatcher.ACTION_MAP", {"PLAY": MagicMock()})
    def test_valid_command_executes(self):
        result = dispatch_command({"command": "PLAY", "confidence": 0.95})
        assert result["status"] == "ok"

    def test_low_confidence_raises(self):
        with pytest.raises(ConfidenceTooLowError):
            dispatch_command({"command": "PLAY", "confidence": 0.50})

    def test_unknown_command_raises(self):
        with pytest.raises(UnknownCommandError):
            dispatch_command({"command": "TELEPORT", "confidence": 0.99})

    @patch("app.dispatcher.ACTION_MAP", {"PAUSE": MagicMock()})
    def test_confidence_at_exact_threshold_passes(self):
        result = dispatch_command({"command": "PAUSE", "confidence": CONFIDENCE_THRESHOLD})
        assert result["status"] == "ok"

    def test_confidence_just_below_threshold_fails(self):
        with pytest.raises(ConfidenceTooLowError):
            dispatch_command({"command": "PAUSE", "confidence": CONFIDENCE_THRESHOLD - 0.01})

    @patch("app.dispatcher.ACTION_MAP", {"CLICK": MagicMock(side_effect=Exception("failsafe"))})
    def test_automation_exception_raises_automation_error(self):
        with pytest.raises(AutomationError):
            dispatch_command({"command": "CLICK", "confidence": 0.9})

    @patch("app.dispatcher.ACTION_MAP", {"PLAY": MagicMock()})
    def test_string_command_accepted(self):
        result = dispatch_command("PLAY", confidence=0.95)
        assert result["status"] == "ok"


# ══════════════════════════════════════════════════════════════════
# 3. API ENDPOINTS
# ══════════════════════════════════════════════════════════════════

class TestAPIEndpoints:

    def test_root_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200
        assert "SynaptiMesh" in r.json()["service"]

    def test_health_returns_200(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"
        assert "mqtt" in r.json()

    @patch("app.server.dispatch_command", return_value={"status": "ok", "message": "ok", "command": "PLAY"})
    @patch("app.server.publish_command")
    def test_receive_command_valid(self, mock_pub, mock_disp):
        r = client.post("/receive-command", json={"command": "PLAY", "confidence": 0.9})
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_receive_command_missing_confidence(self):
        r = client.post("/receive-command", json={"command": "PLAY"})
        assert r.status_code == 422

    def test_receive_command_missing_body(self):
        r = client.post("/receive-command", json={})
        assert r.status_code == 422

    def test_receive_command_invalid_confidence_range(self):
        r = client.post("/receive-command", json={"command": "PLAY", "confidence": 2.0})
        assert r.status_code == 422

    @patch("app.server.dispatch_command", side_effect=ConfidenceTooLowError(0.5, 0.7))
    @patch("app.server.publish_command")
    def test_low_confidence_returns_422(self, mock_pub, mock_disp):
        r = client.post("/receive-command", json={"command": "PLAY", "confidence": 0.5})
        assert r.status_code == 422
        assert r.json()["error"] == "LOW_CONFIDENCE"

    @patch("app.server.dispatch_command", side_effect=UnknownCommandError("TELEPORT"))
    @patch("app.server.publish_command")
    def test_unknown_command_returns_400(self, mock_pub, mock_disp):
        r = client.post("/receive-command", json={"command": "TELEPORT", "confidence": 0.99})
        assert r.status_code == 400
        assert r.json()["error"] == "UNKNOWN_COMMAND"


# ══════════════════════════════════════════════════════════════════
# 4. CHATBOT ENDPOINTS
# ══════════════════════════════════════════════════════════════════

class TestChatbot:

    @patch("app.chatbot.call_groq", new_callable=AsyncMock, return_value="PLAY toggles play/pause.")
    def test_chat_message_endpoint(self, mock_claude):
        r = client.post("/chat/message", json={"message": "What does PLAY do?"})
        assert r.status_code == 200
        assert "reply" in r.json()

    @patch("app.chatbot.call_groq", new_callable=AsyncMock, return_value="Confidence is 0.70.")
    def test_chat_session_endpoint(self, mock_claude):
        r = client.post("/chat/session", json={
            "message": "What is the threshold?",
            "history": []
        })
        assert r.status_code == 200
        assert "reply"   in r.json()
        assert "history" in r.json()

    @patch("app.chatbot.call_groq", new_callable=AsyncMock, return_value="With history.")
    def test_chat_session_preserves_history(self, mock_claude):
        r = client.post("/chat/session", json={
            "message": "What else?",
            "history": [
                {"role": "user",      "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
            ]
        })
        assert r.status_code == 200
        # History in response should include the new exchange
        history = r.json()["history"]
        assert len(history) >= 3

    def test_chat_commands_endpoint(self):
        r = client.get("/chat/commands")
        assert r.status_code == 200
        assert "commands" in r.json()
        assert r.json()["total"] > 0

    def test_chat_message_missing_field(self):
        r = client.post("/chat/message", json={})
        assert r.status_code == 422


# ══════════════════════════════════════════════════════════════════
# 5. EXCEPTION CLASSES
# ══════════════════════════════════════════════════════════════════

class TestExceptions:

    def test_confidence_too_low_code(self):
        e = ConfidenceTooLowError(0.5, 0.7)
        assert e.code == "LOW_CONFIDENCE"
        assert "0.50" in str(e)

    def test_unknown_command_code(self):
        e = UnknownCommandError("TELEPORT")
        assert e.code == "UNKNOWN_COMMAND"
        assert "TELEPORT" in str(e)

    def test_automation_error_code(self):
        e = AutomationError("CLICK", "failsafe triggered")
        assert e.code == "AUTOMATION_ERROR"
        assert "CLICK" in str(e)

    def test_mqtt_publish_error_code(self):
        e = MQTTPublishError("synaptimesh/commands", "timeout")
        assert e.code == "MQTT_PUBLISH_ERROR"

    def test_mqtt_not_connected_error(self):
        e = MQTTNotConnectedError()
        assert e.code == "MQTT_NOT_CONNECTED"

    def test_mqtt_connection_error(self):
        e = MQTTConnectionError("localhost", 1883)
        assert e.code == "MQTT_CONNECTION_ERROR"
        assert "localhost" in str(e)

    def test_invalid_payload_error(self):
        e = InvalidPayloadError("missing command field")
        assert e.code == "INVALID_PAYLOAD"
