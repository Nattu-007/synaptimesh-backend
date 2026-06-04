# tests/test_browser.py
# ⚠️  LIVE TEST — Opens and controls your real browser
# ⚠️  For close/tab tests — move focus away from VS Code after countdown

import time
import platform
from app.schema import validate_command
from app.dispatcher import dispatch_command

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

def test_open_browser():
    countdown(5, "OPEN_BROWSER — browser will launch now")
    result = run("OPEN_BROWSER")
    assert result["status"] == "ok"
    time.sleep(3)   # Wait for browser to fully open
    print(f"✅ OPEN_BROWSER — browser launched on {platform.system()}")

def test_new_tab():
    countdown(5, "NEW_TAB — click on your browser window now!")
    result = run("NEW_TAB")
    assert result["status"] == "ok"
    time.sleep(1)
    print("✅ NEW_TAB — new tab should have opened")

def test_close_tab():
    countdown(5, "CLOSE_TAB — click on your browser window now!")
    result = run("CLOSE_TAB")
    assert result["status"] == "ok"
    time.sleep(1)
    print("✅ CLOSE_TAB — tab should have closed")

def test_close_browser():
    countdown(5, "CLOSE_BROWSER — click on your browser window now! (alt+F4)")
    result = run("CLOSE_BROWSER")
    assert result["status"] == "ok"
    print("✅ CLOSE_BROWSER — focused window should have closed")

def test_skipped_low_confidence():
    countdown(5, "LOW CONFIDENCE — nothing should happen on your PC")
    result = run("OPEN_BROWSER", confidence=0.40)
    assert result["status"] == "skipped"
    print("✅ OPEN_BROWSER skipped — confidence 0.40 below threshold")

def test_exact_threshold():
    countdown(5, "EXACT THRESHOLD — OPEN_BROWSER at exactly 0.70")
    result = run("OPEN_BROWSER", confidence=0.70)
    assert result["status"] == "ok"
    time.sleep(2)
    print("✅ OPEN_BROWSER at exact threshold 0.70 — executed")