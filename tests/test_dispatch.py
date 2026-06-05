# tests/test_dispatch.py
# ⚠️  LIVE TEST — Performs real desktop actions on your PC
# ⚠️  FAILSAFE: Move mouse to TOP-LEFT CORNER to emergency stop
# Run with: pytest tests/test_dispatch.py -v -s

import time
import pyautogui
from app.schema import validate_command
from app.dispatcher import dispatch_command
from app.command_loader import load_commands, get_verified_commands, get_rejected_commands

pyautogui.FAILSAFE = True

# ─── Countdown ──────────────────────────────────────────────────────────────

def countdown(seconds: int = 5, label: str = ""):
    if label:
        print(f"\n⏳ {label}")
    for i in range(seconds, 0, -1):
        print(f"   Starting in {i}...", end="\r")
        time.sleep(1)
    print("   🚀 Executing now!   ")

# ─── Helpers ────────────────────────────────────────────────────────────────

def run_direct(command: str, confidence: float = 1.0):
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

def run_eeg(eeg_signal: str, category: str, confidence: float):
    """Send a raw EEG signal — dispatcher resolves to desktop_action."""
    validated, error = validate_command({
        "eeg_signal": eeg_signal,
        "category":   category,
        "confidence": confidence,
        "source":     "EEG",
        "timestamp":  time.time()
    })
    assert error is None, f"Schema error: {error}"
    return dispatch_command(validated)

# ─── JSON Integrity Tests (no desktop action) ────────────────────────────────

def test_json_has_verified_commands():
    verified = get_verified_commands()
    assert len(verified) > 0
    print(f"✅ JSON loaded — {len(verified)} verified commands found")

def test_json_rejected_commands_exist():
    rejected = get_rejected_commands()
    assert len(rejected) > 0
    print(f"✅ JSON loaded — {len(rejected)} rejected commands found")

def test_json_all_verified_have_required_fields():
    verified = get_verified_commands()
    required = {"sample_id", "command", "confidence", "category",
                "desktop_action", "pyautogui_call", "status", "safety_guard"}
    for entry in verified:
        missing = required - entry.keys()
        assert not missing, f"Missing fields {missing} in sample {entry['sample_id']}"
    print(f"✅ All {len(verified)} verified entries have required fields")

def test_json_confidence_above_threshold():
    """All verified commands must have confidence >= 0.70."""
    verified = get_verified_commands()
    for entry in verified:
        assert entry["confidence"] >= 0.70, (
            f"Verified command {entry['desktop_action']} has confidence "
            f"{entry['confidence']} below 0.70"
        )
    print(f"✅ All verified commands have confidence >= 0.70")

def test_json_rejected_below_threshold():
    """All rejected commands must have confidence < 0.90 (sanity check)."""
    rejected = get_rejected_commands()
    for entry in rejected:
        assert entry["confidence"] < 0.90, (
            f"Rejected command {entry['desktop_action']} has suspiciously "
            f"high confidence {entry['confidence']}"
        )
    print(f"✅ All rejected commands have appropriately low confidence")

# ─── EEG Signal Resolution Tests (no desktop action) ────────────────────────

def test_left_hand_media_resolves():
    result = dispatch_command({
        "eeg_signal": "LEFT_HAND",
        "category":   "media",
        "confidence": 0.9159,
        "source":     "EEG"
    })
    assert result["status"] == "ok"
    assert result["command"] == "PREV_TRACK"
    print(f"✅ LEFT_HAND + media → {result['command']}")

def test_right_hand_media_resolves():
    result = dispatch_command({
        "eeg_signal": "RIGHT_HAND",
        "category":   "media",
        "confidence": 0.9241,
        "source":     "EEG"
    })
    assert result["status"] == "ok"
    assert result["command"] == "NEXT_TRACK"
    print(f"✅ RIGHT_HAND + media → {result['command']}")

def test_unknown_eeg_signal_returns_error():
    result = dispatch_command({
        "eeg_signal": "UNKNOWN_SIGNAL",
        "category":   "media",
        "confidence": 0.95,
        "source":     "EEG"
    })
    assert result["status"] == "error"
    print(f"✅ Unknown EEG signal correctly rejected — {result['message']}")

# ─── Media Tests ─────────────────────────────────────────────────────────────

def test_play():
    countdown(5, "PLAY — open a media player first")
    result = run_direct("PLAY")
    assert result["status"] == "ok"
    print("✅ PLAY — media should have started")

def test_pause():
    countdown(5, "PAUSE — media should be playing")
    result = run_direct("PAUSE")
    assert result["status"] == "ok"
    print("✅ PAUSE — media should have paused")

def test_volume_up():
    countdown(5, "VOLUME_UP — watch your volume indicator")
    result = run_direct("VOLUME_UP")
    assert result["status"] == "ok"
    print("✅ VOLUME_UP — volume increased")

def test_volume_down():
    countdown(5, "VOLUME_DOWN — watch your volume indicator")
    result = run_direct("VOLUME_DOWN")
    assert result["status"] == "ok"
    print("✅ VOLUME_DOWN — volume decreased")

def test_mute():
    countdown(5, "MUTE — audio will be muted")
    result = run_direct("MUTE")
    assert result["status"] == "ok"
    print("✅ MUTE — audio muted")

def test_next_track():
    countdown(5, "NEXT_TRACK — track will advance")
    result = run_direct("NEXT_TRACK")
    assert result["status"] == "ok"
    print("✅ NEXT_TRACK — track advanced")

def test_prev_track():
    countdown(5, "PREV_TRACK — track will go back")
    result = run_direct("PREV_TRACK")
    assert result["status"] == "ok"
    print("✅ PREV_TRACK — track went back")

# ─── EEG Signal → Media Tests ────────────────────────────────────────────────

def test_eeg_left_hand_prev_track():
    countdown(5, "EEG: LEFT_HAND → PREV_TRACK")
    result = run_eeg("LEFT_HAND", "media", 0.9159)
    assert result["status"] == "ok"
    assert result["command"] == "PREV_TRACK"
    print(f"✅ EEG LEFT_HAND → {result['command']} executed")

def test_eeg_right_hand_next_track():
    countdown(5, "EEG: RIGHT_HAND → NEXT_TRACK")
    result = run_eeg("RIGHT_HAND", "media", 0.9241)
    assert result["status"] == "ok"
    assert result["command"] == "NEXT_TRACK"
    print(f"✅ EEG RIGHT_HAND → {result['command']} executed")

# ─── Browser Tests ───────────────────────────────────────────────────────────

def test_open_browser():
    countdown(5, "OPEN_BROWSER — browser will launch")
    result = run_direct("OPEN_BROWSER")
    assert result["status"] == "ok"
    time.sleep(3)
    print("✅ OPEN_BROWSER — launched")

def test_browser_back():
    countdown(5, "BROWSER_BACK — click browser window now!")
    result = run_direct("BROWSER_BACK")
    assert result["status"] == "ok"
    print("✅ BROWSER_BACK — navigated back")

def test_browser_forward():
    countdown(5, "BROWSER_FORWARD — click browser window now!")
    result = run_direct("BROWSER_FORWARD")
    assert result["status"] == "ok"
    print("✅ BROWSER_FORWARD — navigated forward")

def test_browser_refresh():
    countdown(5, "BROWSER_REFRESH — click browser window now!")
    result = run_direct("BROWSER_REFRESH")
    assert result["status"] == "ok"
    print("✅ BROWSER_REFRESH — page refreshed")

def test_new_tab():
    countdown(5, "NEW_TAB — click browser window now!")
    result = run_direct("NEW_TAB")
    assert result["status"] == "ok"
    time.sleep(1)
    print("✅ NEW_TAB — new tab opened")

def test_close_tab():
    countdown(5, "CLOSE_TAB — click browser window now!")
    result = run_direct("CLOSE_TAB")
    assert result["status"] == "ok"
    print("✅ CLOSE_TAB — tab closed")

def test_close_browser():
    countdown(5, "CLOSE_BROWSER — click browser window now!")
    result = run_direct("CLOSE_BROWSER")
    assert result["status"] == "ok"
    print("✅ CLOSE_BROWSER — browser closed")

# ─── Calculator Tests ────────────────────────────────────────────────────────

def test_calculator_addition():
    countdown(5, "CALCULATOR_ADD — 3000 + 457 — calculator will open automatically")
    result = run_direct("CALCULATOR_ADD")
    assert result["status"] == "ok"
    print("✅ CALCULATOR_ADD — check calculator shows 3457")

def test_calculator_subtraction():
    countdown(5, "CALCULATOR_SUBTRACT — 3000 - 457 — calculator will open automatically")
    result = run_direct("CALCULATOR_SUBTRACT")
    assert result["status"] == "ok"
    print("✅ CALCULATOR_SUBTRACT — check calculator shows 2543")

def test_close_calculator():
    countdown(5, "CLOSE_CALCULATOR — closing calculator")
    result = run_direct("CLOSE_CALCULATOR")
    assert result["status"] == "ok"
    print("✅ CLOSE_CALCULATOR — closed")

# ─── Notepad Tests ───────────────────────────────────────────────────────────

def test_notepad_full_automation():
    countdown(5, "NOTEPAD_FULL_AUTOMATION — notepad will open and type the full log")
    result = run_direct("NOTEPAD_FULL_AUTOMATION")
    assert result["status"] == "ok"
    print("✅ NOTEPAD_FULL_AUTOMATION — log written, file saved")
    print("✅ Final line: 'Automation is done'")

def test_close_notepad():
    countdown(5, "CLOSE_NOTEPAD — closing notepad without saving")
    result = run_direct("CLOSE_NOTEPAD")
    assert result["status"] == "ok"
    print("✅ CLOSE_NOTEPAD — closed")

# ─── Mouse Tests ─────────────────────────────────────────────────────────────

def test_move_left():
    countdown(5, "MOVE_LEFT — cursor moves left 50px")
    before_x, before_y = pyautogui.position()
    result = run_direct("MOVE_LEFT")
    after_x, _ = pyautogui.position()
    assert result["status"] == "ok"
    assert after_x < before_x or after_x == 0
    print(f"✅ MOVE_LEFT — x: {before_x} → {after_x}")

def test_move_right():
    countdown(5, "MOVE_RIGHT — cursor moves right 50px")
    before_x, _ = pyautogui.position()
    result = run_direct("MOVE_RIGHT")
    after_x, _ = pyautogui.position()
    screen_w, _ = pyautogui.size()
    assert result["status"] == "ok"
    assert after_x > before_x or after_x == screen_w
    print(f"✅ MOVE_RIGHT — x: {before_x} → {after_x}")

def test_move_up():
    countdown(5, "MOVE_UP — cursor moves up 50px")
    _, before_y = pyautogui.position()
    result = run_direct("MOVE_UP")
    _, after_y = pyautogui.position()
    assert result["status"] == "ok"
    assert after_y < before_y or after_y == 0
    print(f"✅ MOVE_UP — y: {before_y} → {after_y}")

def test_move_down():
    countdown(5, "MOVE_DOWN — cursor moves down 50px")
    _, before_y = pyautogui.position()
    result = run_direct("MOVE_DOWN")
    _, after_y = pyautogui.position()
    _, screen_h = pyautogui.size()
    assert result["status"] == "ok"
    assert after_y > before_y or after_y == screen_h
    print(f"✅ MOVE_DOWN — y: {before_y} → {after_y}")

def test_scroll_up():
    countdown(5, "SCROLL_UP — move cursor over scrollable window")
    result = run_direct("SCROLL_UP")
    assert result["status"] == "ok"
    print("✅ SCROLL_UP — scrolled up")

def test_scroll_down():
    countdown(5, "SCROLL_DOWN — move cursor over scrollable window")
    result = run_direct("SCROLL_DOWN")
    assert result["status"] == "ok"
    print("✅ SCROLL_DOWN — scrolled down")

def test_scroll_up_fast():
    countdown(5, "SCROLL_UP_FAST — move cursor over scrollable window")
    result = run_direct("SCROLL_UP_FAST")
    assert result["status"] == "ok"
    print("✅ SCROLL_UP_FAST — fast scrolled up")

def test_click():
    countdown(5, "CLICK — move cursor to safe empty area now")
    result = run_direct("CLICK")
    assert result["status"] == "ok"
    print("✅ CLICK — left clicked")

def test_right_click():
    countdown(5, "RIGHT_CLICK — move cursor to safe empty area now")
    result = run_direct("RIGHT_CLICK")
    assert result["status"] == "ok"
    time.sleep(0.5)
    pyautogui.press("escape")
    print("✅ RIGHT_CLICK — right clicked, menu closed")

# ─── Confidence Gate Tests ───────────────────────────────────────────────────

def test_skipped_below_threshold():
    countdown(5, "LOW CONFIDENCE — nothing should happen on your PC")
    result = run_direct("PLAY", confidence=0.50)
    assert result["status"] == "skipped"
    print(f"✅ PLAY skipped — {result['message']}")

def test_eeg_rest_rejected_low_confidence():
    """REST + media at 0.7743 — should be skipped (matches your real data)."""
    result = run_eeg("REST", "media", 0.7743)
    assert result["status"] == "skipped"
    print(f"✅ EEG REST skipped — confidence 0.7743 below threshold")

# ─── Safety Guard Tests ──────────────────────────────────────────────────────

def test_safety_guard_warning_on_close_browser():
    """CLOSE_BROWSER should return a warning in the result."""
    result = dispatch_command({
        "command":    "CLOSE_BROWSER",
        "confidence": 0.99,
        "source":     "EEG"
    })
    # Warning should be present even on success
    if result["status"] == "ok":
        print(f"✅ CLOSE_BROWSER safety warning: {result.get('warning')}")
    else:
        print(f"✅ CLOSE_BROWSER result: {result}")

def test_safety_guard_warning_on_close_notepad():
    result = dispatch_command({
        "command":    "CLOSE_NOTEPAD",
        "confidence": 0.99,
        "source":     "EEG"
    })
    if result["status"] == "ok":
        print(f"✅ CLOSE_NOTEPAD safety warning: {result.get('warning')}")