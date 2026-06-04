# tests/test_media.py
# ⚠️  LIVE TEST — Opens real media keys on your PC
# Have a media player (VLC, Spotify, YouTube) open and playing before running

import time
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

def test_play():
    countdown(5, "PLAY — make sure media player is open and paused")
    result = run("PLAY")
    assert result["status"] == "ok"
    print("✅ PLAY — check if media started")

def test_pause():
    countdown(5, "PAUSE — media should be playing")
    result = run("PAUSE")
    assert result["status"] == "ok"
    print("✅ PAUSE — check if media paused")

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
    result = run("MUTE")
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
    countdown(5, "STOP — media will stop")
    result = run("STOP")
    assert result["status"] == "ok"
    print("✅ STOP — media should have stopped")

def test_skipped_low_confidence():
    countdown(5, "LOW CONFIDENCE — nothing should happen on your PC")
    result = run("PLAY", confidence=0.50)
    assert result["status"] == "skipped"
    print("✅ PLAY skipped — confidence 0.50 below threshold")

def test_exact_threshold():
    countdown(5, "EXACT THRESHOLD — PLAY at exactly 0.70")
    result = run("PLAY", confidence=0.70)
    assert result["status"] == "ok"
    print("✅ PLAY at exact threshold 0.70 — executed")