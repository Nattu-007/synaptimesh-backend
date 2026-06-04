# tests/test_dispatch.py
# ⚠️  LIVE TEST — Performs real desktop actions on your PC
# ⚠️  FAILSAFE: Move mouse to TOP-LEFT CORNER to emergency stop
# ⚠️  Always run with: pytest tests/test_dispatch.py -v -s

import time
import pyautogui
from app.schema import validate_command
from app.dispatcher import dispatch_command

pyautogui.FAILSAFE = True  # TOP-LEFT CORNER = emergency abort

# ─── Countdown ──────────────────────────────────────────────────────────────

def countdown(seconds: int = 5, label: str = ""):
    if label:
        print(f"\n⏳ {label}")
    for i in range(seconds, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    print("   🚀 Executing now!   ")

# ─── Helper ─────────────────────────────────────────────────────────────────

def run(command: str, confidence: float = 0.95, source: str = "EEG"):
    validated, error = validate_command({
        "command":    command,
        "confidence": confidence,
        "source":     source,
        "timestamp":  time.time()
    })
    assert error is None, f"Schema error: {error}"
    return dispatch_command(validated)

# ─── Media Tests ────────────────────────────────────────────────────────────

def test_play():
    countdown(5, "PLAY — make sure a media player is open and paused")
    result = run("PLAY")
    assert result["status"] == "ok"
    print("✅ PLAY — media should have started")

def test_pause():
    countdown(5, "PAUSE — media should be playing")
    result = run("PAUSE")
    assert result["status"] == "ok"
    print("✅ PAUSE — media should have paused")

def test_volume_up():
    countdown(5, "VOLUME_UP — watch your system volume indicator")
    result = run("VOLUME_UP")
    assert result["status"] == "ok"
    print("✅ VOLUME_UP — volume should have increased")

def test_volume_down():
    countdown(5, "VOLUME_DOWN — watch your system volume indicator")
    result = run("VOLUME_DOWN")
    assert result["status"] == "ok"
    print("✅ VOLUME_DOWN — volume should have decreased")

def test_mute():
    countdown(5, "MUTE — audio will be muted")
    result = run("MUTE")
    assert result["status"] == "ok"
    print("✅ MUTE — audio should be muted")

def test_unmute():
    countdown(5, "UNMUTE — audio will be restored")
    result = run("MUTE")   # Second press toggles back
    assert result["status"] == "ok"
    print("✅ UNMUTE — audio should be restored")

def test_next_track():
    countdown(5, "NEXT_TRACK — track will advance")
    result = run("NEXT_TRACK")
    assert result["status"] == "ok"
    print("✅ NEXT_TRACK — track should have advanced")

def test_prev_track():
    countdown(5, "PREV_TRACK — track will go back")
    result = run("PREV_TRACK")
    assert result["status"] == "ok"
    print("✅ PREV_TRACK — track should have gone back")

def test_stop():
    countdown(5, "STOP — media will stop completely")
    result = run("STOP")
    assert result["status"] == "ok"
    print("✅ STOP — media should have stopped")

# ─── Browser Tests ──────────────────────────────────────────────────────────

def test_open_browser():
    countdown(5, "OPEN_BROWSER — browser will launch now")
    result = run("OPEN_BROWSER")
    assert result["status"] == "ok"
    time.sleep(3)   # Wait for browser to fully open
    print("✅ OPEN_BROWSER — browser should have launched")

def test_new_tab():
    countdown(5, "NEW_TAB — click your browser window now!")
    result = run("NEW_TAB")
    assert result["status"] == "ok"
    time.sleep(1)
    print("✅ NEW_TAB — new tab should have opened")

def test_close_tab():
    countdown(5, "CLOSE_TAB — click your browser window now!")
    result = run("CLOSE_TAB")
    assert result["status"] == "ok"
    time.sleep(1)
    print("✅ CLOSE_TAB — tab should have closed")

def test_close_browser():
    countdown(5, "CLOSE_BROWSER — click your browser window now! (alt+F4)")
    result = run("CLOSE_BROWSER")
    assert result["status"] == "ok"
    print("✅ CLOSE_BROWSER — browser window should have closed")

# ─── Mouse Tests ────────────────────────────────────────────────────────────

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
    after_x, _ = pyautogui.position()
    assert result["status"] == "ok"
    assert after_x < before_x or after_x == 0
    print(f"✅ MOVE_LEFT — cursor moved from x={before_x} to x={after_x}")

def test_move_right():
    countdown(5, "MOVE_RIGHT — cursor will move right by 50px")
    before_x, before_y = pyautogui.position()
    result = run("MOVE_RIGHT")
    after_x, _ = pyautogui.position()
    screen_w, _ = pyautogui.size()
    assert result["status"] == "ok"
    assert after_x > before_x or after_x == screen_w
    print(f"✅ MOVE_RIGHT — cursor moved from x={before_x} to x={after_x}")

def test_click():
    countdown(5, "CLICK — move cursor to a safe empty area now")
    result = run("CLICK")
    assert result["status"] == "ok"
    print("✅ CLICK — left click executed at cursor position")

def test_right_click():
    countdown(5, "RIGHT_CLICK — move cursor to a safe empty area now")
    result = run("RIGHT_CLICK")
    assert result["status"] == "ok"
    time.sleep(0.5)
    pyautogui.press("escape")   # Close context menu that opened
    print("✅ RIGHT_CLICK — context menu appeared then closed")

# ─── Confidence Gate Tests ──────────────────────────────────────────────────

def test_skipped_below_threshold():
    countdown(5, "LOW CONFIDENCE (0.50) — nothing should happen on your PC")
    result = run("PLAY", confidence=0.50)
    assert result["status"] == "skipped"
    assert "0.50" in result["message"]
    print("✅ PLAY skipped — confidence 0.50 below threshold 0.70")

def test_skipped_zero_confidence():
    countdown(5, "ZERO CONFIDENCE — nothing should happen on your PC")
    result = run("SCROLL_UP", confidence=0.00)
    assert result["status"] == "skipped"
    print("✅ SCROLL_UP skipped — confidence 0.00")

def test_exact_threshold_passes():
    countdown(5, "EXACT THRESHOLD (0.70) — PLAY should execute")
    result = run("PLAY", confidence=0.70)
    assert result["status"] == "ok"
    print("✅ PLAY at exact threshold 0.70 — executed correctly")

def test_just_below_threshold_skipped():
    countdown(5, "JUST BELOW THRESHOLD (0.69) — nothing should happen")
    result = run("PLAY", confidence=0.69)
    assert result["status"] == "skipped"
    print("✅ PLAY skipped — confidence 0.69 just below threshold")

# ─── Schema Validation Tests (no timer needed — no desktop action) ──────────

def test_schema_missing_confidence():
    result_tuple = validate_command({"command": "PLAY"})
    validated, error = result_tuple
    assert validated is None
    assert error is not None
    print(f"✅ Schema error caught — {error}")

def test_schema_missing_command():
    validated, error = validate_command({"confidence": 0.95})
    assert validated is None
    assert error is not None
    print(f"✅ Schema error caught — {error}")

def test_schema_invalid_confidence_type():
    validated, error = validate_command({"command": "PLAY", "confidence": "high"})
    assert validated is None
    assert error is not None
    print(f"✅ Schema error caught — {error}")

def test_unknown_command():
    validated, error = validate_command({"command": "UNKNOWN_CMD", "confidence": 0.99})
    assert error is None
    result = dispatch_command(validated)
    assert result["status"] == "error"
    assert "Unknown" in result["message"]
    print(f"✅ Unknown command rejected — {result['message']}")

def test_optional_fields_accepted():
    validated, error = validate_command({
        "command":    "MUTE",
        "confidence": 0.85,
        "timestamp":  1717401600.0,
        "source":     "EEG"
    })
    assert error is None
    assert validated["source"] == "EEG"
    assert validated["timestamp"] == 1717401600.0
    print("✅ Optional fields (timestamp, source) accepted correctly")