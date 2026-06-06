# demo_runner.py
# Synaptimesh Sprint 3 Demo — Day 4
# Runs a full end-to-end test including chatbot
# Run: python demo_runner.py

import json
import time
import uuid
import requests

BASE_URL = "http://127.0.0.1:5000"
DIVIDER  = "─" * 60

DEMO_COMMANDS = [
    # (command, confidence, expected)
    ("PLAY",                 0.92, "success"),
    ("PAUSE",                0.87, "success"),
    ("VOLUME_UP",            0.95, "success"),
    ("NEXT_TRACK",           0.93, "success"),
    ("OPEN_BROWSER",         0.88, "success"),
    ("SCROLL_UP",            0.91, "success"),
    ("OPEN_CALCULATOR",      0.85, "success"),
    ("OPEN_NOTEPAD",         0.89, "success"),
    ("MOVE_RIGHT",           0.82, "success"),
    ("MUTE",                 0.90, "success"),
    # Edge cases
    ("PAUSE",                0.55, "rejected"),  # low confidence
    ("TELEPORT",             0.99, "rejected"),  # unknown command
]

CHATBOT_QUESTIONS = [
    "What does the PLAY command do?",
    "Why would a command be rejected?",
    "What EEG signal maps to NEXT_TRACK in media mode?",
]


def print_header():
    print("\n" + "═" * 60)
    print("   SYNAPTIMESH — Sprint 3 Demo Runner  (Day 4)")
    print("   EEG Command Pipeline + Chatbot Test")
    print("═" * 60)


def check_health() -> bool:
    print("\n[ HEALTH CHECK ]")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=3)
        d = r.json()
        print(f"  Status : {d.get('status','?').upper()}")
        print(f"  MQTT   : {d.get('mqtt','?').upper()}")
        return True
    except Exception as e:
        print(f"  ✗ Server not reachable — {e}")
        return False


def send_command(command, confidence, expected) -> bool:
    payload = {
        "command":        command,
        "confidence":     confidence,
        "source":         "demo_runner",
    }
    try:
        r    = requests.post(f"{BASE_URL}/receive-command", json=payload, timeout=5)
        data = r.json()
        ok   = (expected == "success" and r.status_code == 200) or \
               (expected == "rejected" and r.status_code != 200)

        icon = "✓" if ok else "✗"
        print(f"  {icon} {command:<25} conf={confidence:.2f}  HTTP {r.status_code}", end="")
        if r.status_code == 200:
            print(f"  dispatch={data.get('dispatch', {}).get('status','?')}")
        else:
            print(f"  [{data.get('error','?')}]")
        return ok
    except Exception as e:
        print(f"  ✗ {command:<25} ERROR: {e}")
        return False


def test_chatbot():
    print(f"\n[ CHATBOT TEST ]")
    passed = 0
    for q in CHATBOT_QUESTIONS:
        try:
            r = requests.post(
                f"{BASE_URL}/chat/message",
                json={"message": q},
                timeout=15,
            )
            if r.status_code == 200 and r.json().get("reply"):
                reply_preview = r.json()["reply"][:80].replace("\n", " ")
                print(f"  ✓ Q: {q[:50]}")
                print(f"    A: {reply_preview}...")
                passed += 1
            else:
                print(f"  ✗ Q: {q[:50]} — HTTP {r.status_code}")
        except Exception as e:
            print(f"  ✗ Chatbot error: {e}")
        time.sleep(0.5)
    return passed, len(CHATBOT_QUESTIONS)


def run_demo():
    print_header()
    if not check_health():
        print("  Aborting — start the server first:")
        print("  python -m app.server\n")
        return

    print(f"\n[ COMMAND PIPELINE — {len(DEMO_COMMANDS)} commands ]\n")
    cmd_passed = 0
    for command, confidence, expected in DEMO_COMMANDS:
        if send_command(command, confidence, expected):
            cmd_passed += 1
        time.sleep(0.3)

    chat_passed, chat_total = test_chatbot()

    print(f"\n{DIVIDER}")
    print(f"  Commands : {cmd_passed}/{len(DEMO_COMMANDS)} passed")
    print(f"  Chatbot  : {chat_passed}/{chat_total} passed")
    total_p = cmd_passed + chat_passed
    total_t = len(DEMO_COMMANDS) + chat_total
    if total_p == total_t:
        print(f"  Overall  : {total_p}/{total_t} ✓ ALL PASSED — Demo ready!")
    else:
        print(f"  Overall  : {total_p}/{total_t} — review logs/command_log.txt")
    print(DIVIDER + "\n")


if __name__ == "__main__":
    run_demo()
