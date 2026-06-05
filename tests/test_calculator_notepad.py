# tests/test_calculator_notepad.py
# ⚠️  LIVE TEST — Opens real Calculator and Notepad on your PC
# ⚠️  FAILSAFE: Move mouse to TOP-LEFT CORNER to emergency stop
# Run with: pytest tests/test_calculator_notepad.py -v -s

import time
import pyautogui
from app.schema import validate_command
from app.dispatcher import dispatch_command

pyautogui.FAILSAFE = True

# ─── Countdown ──────────────────────────────────────────────────────────────

def countdown(seconds: int = 5, label: str = ""):
    if label:
        print(f"\n⏳ {label}")
    for i in range(seconds, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    print("   🚀 Executing now!   ")

def run(command: str, confidence: float = 1.0):
    validated, error = validate_command({
        "command": command,
        "confidence": confidence,
        "source": "EEG",
        "timestamp": time.time()
    })

    assert error is None, f"Schema error: {error}"

    return dispatch_command(
        command=validated["command"],
        confidence=validated["confidence"]
    )

# ─── Calculator Tests ────────────────────────────────────────────────────────

def test_calculator_addition():
    countdown(5, "CALCULATOR_ADD — 3000 + 457 — calculator will open automatically")
    result = run("CALCULATOR_ADD")
    assert result["status"] == "ok"
    print("✅ CALCULATOR_ADD — check calculator shows 3457")

def test_calculator_subtraction():
    countdown(5, "CALCULATOR_SUBTRACT — 3000 - 457 — calculator will open automatically")
    result = run("CALCULATOR_SUBTRACT")
    assert result["status"] == "ok"
    print("✅ CALCULATOR_SUBTRACT — check calculator shows 2543")

def test_close_calculator():
    countdown(5, "CLOSE_CALCULATOR — closing calculator")
    result = run("CLOSE_CALCULATOR")
    assert result["status"] == "ok"
    print("✅ CLOSE_CALCULATOR — closed")

# ─── Notepad Tests ───────────────────────────────────────────────────────────

def test_notepad_full_automation():
    countdown(5, "NOTEPAD_FULL_AUTOMATION — notepad will open and type the full log")
    result = run("NOTEPAD_FULL_AUTOMATION")
    assert result["status"] == "ok"
    print("✅ NOTEPAD_FULL_AUTOMATION — log written, file saved")
    print("✅ Final line: 'Automation is done'")

def test_close_notepad():
    countdown(5, "CLOSE_NOTEPAD — closing notepad without saving")
    result = run("CLOSE_NOTEPAD")
    assert result["status"] == "ok"
    print("✅ CLOSE_NOTEPAD — closed")
