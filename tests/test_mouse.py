# tests/test_mouse.py
# ⚠️  LIVE TEST — Moves your real mouse and clicks on your PC
# ⚠️  FAILSAFE: Move mouse to TOP-LEFT CORNER to emergency stop
# Keep cursor over a safe empty area during countdown

import time
import pyautogui
from app.schema import validate_command
from app.dispatcher import dispatch_command

pyautogui.FAILSAFE = True   # TOP-LEFT CORNER = emergency abort

# ─── Countdown ──────────────────────────────────────────────────────────────

def countdown(seconds: int = 5, label: str = ""):
    if label:
        print(f"\n⏳ {label}")
    for i in range(seconds, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    print("   🚀 Executing now!   ")

# ─── Helper ─────────────────────────────────────────────────────────────────

def run(command: str, confidence: float = 0.95):
    validated, error = validate_command({"command": command, "confidence": confidence})
    assert error is None, f"Schema error: {error}"
    return dispatch_command(validated)

# ─── Tests ──────────────────────────────────────────────────────────────────

def test_scroll_up():
    countdown(5, "SCROLL_UP — move cursor over a scrollable window now")
    result = run("SCROLL_UP")
    assert result["status"] == "ok"
    print("✅ SCROLL_UP — page should have scrolled up")

def test_scroll_down():
    countdown(5, "SCROLL_DOWN — move cursor over a scrollable window now")
    result = run("SCROLL_DOWN")
    assert result["status"] == "ok"
    print("✅ SCROLL_DOWN — page should have scrolled down")

def test_move_left():
    countdown(5, "MOVE_LEFT — cursor will move left by 50px")
    before_x, before_y = pyautogui.position()
    result = run("MOVE_LEFT")
    after_x, after_y = pyautogui.position()
    assert result["status"] == "ok"
    assert after_x < before_x or after_x == 0
    print(f"✅ MOVE_LEFT — cursor moved from x={before_x} to x={after_x}")

def test_move_right():
    countdown(5, "MOVE_RIGHT — cursor will move right by 50px")
    before_x, before_y = pyautogui.position()
    result = run("MOVE_RIGHT")
    after_x, after_y = pyautogui.position()
    assert result["status"] == "ok"
    screen_w, _ = pyautogui.size()
    assert after_x > before_x or after_x == screen_w
    print(f"✅ MOVE_RIGHT — cursor moved from x={before_x} to x={after_x}")

def test_move_left_clamped():
    countdown(5, "MOVE_LEFT CLAMP — cursor will be forced near left edge")
    pyautogui.moveTo(10, 400, duration=0.2)
    time.sleep(0.3)
    result = run("MOVE_LEFT")
    x, _ = pyautogui.position()
    assert result["status"] == "ok"
    assert x >= 0
    print(f"✅ MOVE_LEFT clamped — cursor at x={x}, did not go negative")

def test_move_right_clamped():
    countdown(5, "MOVE_RIGHT CLAMP — cursor will be forced near right edge")
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(screen_w - 10, 400, duration=0.2)
    time.sleep(0.3)
    result = run("MOVE_RIGHT")
    x, _ = pyautogui.position()
    assert result["status"] == "ok"
    assert x <= screen_w
    print(f"✅ MOVE_RIGHT clamped — cursor at x={x}, did not exceed screen width {screen_w}")

def test_right_click():
    countdown(5, "RIGHT_CLICK — move cursor to a safe empty area now")
    result = run("RIGHT_CLICK")
    assert result["status"] == "ok"
    time.sleep(0.5)
    pyautogui.press("escape")   # Close context menu
    print("✅ RIGHT_CLICK — context menu appeared then closed")

def test_click():
    countdown(5, "CLICK — move cursor to a safe empty area now")
    result = run("CLICK")
    assert result["status"] == "ok"
    print("✅ CLICK — left click executed at cursor position")

def test_skipped_low_confidence():
    countdown(5, "LOW CONFIDENCE — nothing should happen on your PC")
    before_x, before_y = pyautogui.position()
    result = run("SCROLL_UP", confidence=0.30)
    after_x, after_y = pyautogui.position()
    assert result["status"] == "skipped"
    assert before_x == after_x and before_y == after_y
    print("✅ SCROLL_UP skipped — confidence 0.30, cursor did not move")

def test_exact_threshold():
    countdown(5, "EXACT THRESHOLD — SCROLL_UP at exactly 0.70")
    result = run("SCROLL_UP", confidence=0.70)
    assert result["status"] == "ok"
    print("✅ SCROLL_UP at exact threshold 0.70 — executed")