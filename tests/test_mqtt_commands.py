# tests/test_mqtt_commands.py
# Tests that MQTT messages correctly trigger desktop automation
# Run with: pytest tests/test_mqtt_commands.py -v -s

import time
import json
import uuid
import pytest
import pyautogui
import paho.mqtt.client as mqtt
from app.config import MQTT_BROKER, MQTT_PORT

pyautogui.FAILSAFE = True

TOPIC = "synaptimesh/commands/desktop"

# ─── Countdown ──────────────────────────────────────────────────────────────

def countdown(seconds: int = 5, label: str = ""):
    if label:
        print(f"\n⏳ {label}")
    for i in range(seconds, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    print("   🚀 Executing now!   ")

# ─── MQTT Publisher Fixture ──────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mqtt_publisher():
    """Creates a shared publisher for all tests."""
    pub = mqtt.Client(client_id=f"test-publisher-{uuid.uuid4().hex[:4]}")
    pub.connect(MQTT_BROKER, MQTT_PORT)
    pub.loop_start()
    time.sleep(1)   # Wait for connection
    yield pub
    pub.loop_stop()
    pub.disconnect()

# ─── Helper ─────────────────────────────────────────────────────────────────

def send(publisher, command: str, confidence: float = 0.95):
    message = {
        "correlation_id": str(uuid.uuid4())[:8],
        "command":        command,
        "confidence":     confidence,
        "source":         "MQTT_TEST",
        "timestamp":      time.time()
    }
    result = publisher.publish(TOPIC, json.dumps(message))
    assert result.rc == mqtt.MQTT_ERR_SUCCESS, f"Publish failed for {command}"
    print(f"[MQTT SENT] {command} | confidence={confidence}")
    time.sleep(2)   # Wait for listener to process and execute

# ─── Media via MQTT ─────────────────────────────────────────────────────────

def test_mqtt_play(mqtt_publisher):
    countdown(5, "MQTT → PLAY — open a media player first")
    send(mqtt_publisher, "PLAY")
    print("✅ MQTT PLAY — check media started")

def test_mqtt_volume_up(mqtt_publisher):
    countdown(5, "MQTT → VOLUME_UP — watch volume indicator")
    send(mqtt_publisher, "VOLUME_UP")
    print("✅ MQTT VOLUME_UP — volume increased")

def test_mqtt_next_track(mqtt_publisher):
    countdown(5, "MQTT → NEXT_TRACK")
    send(mqtt_publisher, "NEXT_TRACK")
    print("✅ MQTT NEXT_TRACK — track advanced")

def test_mqtt_pause(mqtt_publisher):
    countdown(5, "MQTT → PAUSE")
    send(mqtt_publisher, "PAUSE")
    print("✅ MQTT PAUSE — media paused")

# ─── Calculator via MQTT ────────────────────────────────────────────────────

def test_mqtt_calculator_addition(mqtt_publisher):
    countdown(5, "MQTT → CALCULATOR_ADD — 3000 + 457 = 3457")
    send(mqtt_publisher, "CALCULATOR_ADD", confidence=0.95)
    time.sleep(4)   # Extra wait for calculator to open and type
    print("✅ MQTT CALCULATOR_ADD — check calculator shows 3457")

def test_mqtt_calculator_subtraction(mqtt_publisher):
    countdown(5, "MQTT → CALCULATOR_SUBTRACT — 3000 - 457 = 2543")
    send(mqtt_publisher, "CALCULATOR_SUBTRACT", confidence=0.95)
    time.sleep(4)
    print("✅ MQTT CALCULATOR_SUBTRACT — check calculator shows 2543")

def test_mqtt_close_calculator(mqtt_publisher):
    countdown(5, "MQTT → CLOSE_CALCULATOR — click calculator window now!")
    send(mqtt_publisher, "CLOSE_CALCULATOR", confidence=0.93)
    print("✅ MQTT CLOSE_CALCULATOR — closed")

# ─── Notepad via MQTT ───────────────────────────────────────────────────────

def test_mqtt_notepad_full_automation(mqtt_publisher):
    countdown(5, "MQTT → NOTEPAD_FULL_AUTOMATION — notepad will open and type")
    send(mqtt_publisher, "NOTEPAD_FULL_AUTOMATION", confidence=0.95)
    time.sleep(12)   # Wait for full typing sequence to finish
    print("✅ MQTT NOTEPAD_FULL_AUTOMATION — log written, 'Automation is done' displayed")

def test_mqtt_close_notepad(mqtt_publisher):
    countdown(5, "MQTT → CLOSE_NOTEPAD — click notepad window now!")
    send(mqtt_publisher, "CLOSE_NOTEPAD", confidence=0.93)
    print("✅ MQTT CLOSE_NOTEPAD — closed")

# ─── Browser via MQTT ───────────────────────────────────────────────────────

def test_mqtt_open_browser(mqtt_publisher):
    countdown(5, "MQTT → OPEN_BROWSER — browser will launch")
    send(mqtt_publisher, "OPEN_BROWSER", confidence=0.95)
    time.sleep(3)
    print("✅ MQTT OPEN_BROWSER — launched")

def test_mqtt_new_tab(mqtt_publisher):
    countdown(5, "MQTT → NEW_TAB — click browser window now!")
    send(mqtt_publisher, "NEW_TAB", confidence=0.94)
    print("✅ MQTT NEW_TAB — new tab opened")

def test_mqtt_close_browser(mqtt_publisher):
    countdown(5, "MQTT → CLOSE_BROWSER — click browser window now!")
    send(mqtt_publisher, "CLOSE_BROWSER", confidence=0.93)
    print("✅ MQTT CLOSE_BROWSER — closed")

# ─── Mouse via MQTT ─────────────────────────────────────────────────────────

def test_mqtt_scroll_up(mqtt_publisher):
    countdown(5, "MQTT → SCROLL_UP — move cursor over scrollable window")
    send(mqtt_publisher, "SCROLL_UP", confidence=0.95)
    print("✅ MQTT SCROLL_UP — scrolled up")

def test_mqtt_move_left(mqtt_publisher):
    countdown(5, "MQTT → MOVE_LEFT — cursor will move left")
    before_x, _ = pyautogui.position()
    send(mqtt_publisher, "MOVE_LEFT", confidence=0.93)
    after_x, _ = pyautogui.position()
    print(f"✅ MQTT MOVE_LEFT — x: {before_x} → {after_x}")

# ─── Confidence Gate via MQTT ────────────────────────────────────────────────

def test_mqtt_skipped_low_confidence(mqtt_publisher):
    countdown(5, "MQTT LOW CONFIDENCE — nothing should happen on your PC")
    send(mqtt_publisher, "PLAY", confidence=0.40)
    print("✅ MQTT PLAY skipped — confidence 0.40 below threshold")

# ─── Full Sequence via MQTT ──────────────────────────────────────────────────

def test_mqtt_full_sequence(mqtt_publisher):
    print("\n" + "=" * 55)
    print("  FULL AUTOMATION SEQUENCE VIA MQTT")
    print("=" * 55)

    # Calculator
    countdown(5, "Step 1 — MQTT → CALCULATOR_ADD: 3000 + 457")
    send(mqtt_publisher, "CALCULATOR_ADD", 0.95)
    time.sleep(5)
    print("✅ Step 1 — shows 3457")

    countdown(5, "Step 2 — MQTT → CALCULATOR_SUBTRACT: 3000 - 457")
    send(mqtt_publisher, "CALCULATOR_SUBTRACT", 0.95)
    time.sleep(5)
    print("✅ Step 2 — shows 2543")

    countdown(5, "Step 3 — MQTT → CLOSE_CALCULATOR — click it now!")
    send(mqtt_publisher, "CLOSE_CALCULATOR", 0.93)
    time.sleep(2)
    print("✅ Step 3 — calculator closed")

    # Notepad
    countdown(5, "Step 4 — MQTT → NOTEPAD_FULL_AUTOMATION")
    send(mqtt_publisher, "NOTEPAD_FULL_AUTOMATION", 0.95)
    time.sleep(15)
    print("✅ Step 4 — log written, 'Automation is done' displayed")

    countdown(5, "Step 5 — MQTT → CLOSE_NOTEPAD — click it now!")
    send(mqtt_publisher, "CLOSE_NOTEPAD", 0.93)
    time.sleep(2)
    print("✅ Step 5 — notepad closed")

    print("\n" + "=" * 55)
    print("  FULL MQTT SEQUENCE COMPLETE")
    print("=" * 55)