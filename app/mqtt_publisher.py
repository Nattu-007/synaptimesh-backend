# app/mqtt_publisher.py
# Use this to publish commands from the terminal
# python -m app.mqtt_publisher

import paho.mqtt.client as mqtt
import json
import uuid
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.config import MQTT_BROKER, MQTT_PORT

TOPIC = "synaptimesh/commands/desktop"

publisher = mqtt.Client(client_id="synaptimesh-publisher")
publisher.connect(MQTT_BROKER, MQTT_PORT)
publisher.loop_start()
time.sleep(0.5)

def publish(command: str, confidence: float = 0.95, category: str = "desktop"):
    message = {
        "correlation_id": str(uuid.uuid4())[:8],
        "command":        command,
        "confidence":     confidence,
        "source":         "MQTT_TERMINAL",
        "timestamp":      time.time(),
        "target":         category
    }
    payload = json.dumps(message)
    result  = publisher.publish(TOPIC, payload)

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"[SENT] {command} → {TOPIC}")
    else:
        print(f"[FAILED] {command} — rc={result.rc}")

# ─── Command Sequences ───────────────────────────────────────────────────────

def run_media_sequence():
    print("\n── Media Sequence ──")
    commands = [
        ("PLAY",        0.95),
        ("VOLUME_UP",   0.94),
        ("VOLUME_UP",   0.94),
        ("NEXT_TRACK",  0.93),
        ("PREV_TRACK",  0.91),
        ("VOLUME_DOWN", 0.92),
        ("MUTE",        0.90),
        ("MUTE",        0.90),   # Unmute
        ("PAUSE",       0.88),
    ]
    for cmd, conf in commands:
        publish(cmd, conf)
        time.sleep(2)            # 2 seconds between each command

def run_calculator_sequence():
    print("\n── Calculator Sequence ──")
    publish("OPEN_CALCULATOR", 0.96)
    time.sleep(3)                # Wait for calculator to open
    publish("CALCULATOR_ADD", 0.95)
    time.sleep(4)                # Wait for addition to complete
    publish("CALCULATOR_SUBTRACT", 0.95)
    time.sleep(4)                # Wait for subtraction to complete
    publish("CLOSE_CALCULATOR", 0.93)
    time.sleep(1)

def run_notepad_sequence():
    print("\n── Notepad Sequence ──")
    publish("OPEN_NOTEPAD", 0.96)
    time.sleep(3)                # Wait for notepad to open
    publish("NOTEPAD_FULL_AUTOMATION", 0.95)
    time.sleep(10)               # Wait for full typing to complete
    publish("CLOSE_NOTEPAD", 0.93)
    time.sleep(1)

def run_browser_sequence():
    print("\n── Browser Sequence ──")
    publish("OPEN_BROWSER", 0.95)
    time.sleep(4)                # Wait for browser to open
    publish("NEW_TAB", 0.94)
    time.sleep(1)
    publish("BROWSER_REFRESH", 0.92)
    time.sleep(1)
    publish("BROWSER_BACK", 0.91)
    time.sleep(1)
    publish("CLOSE_TAB", 0.90)
    time.sleep(1)
    publish("CLOSE_BROWSER", 0.93)
    time.sleep(1)

def run_mouse_sequence():
    print("\n── Mouse Sequence ──")
    commands = [
        ("SCROLL_UP",   0.95),
        ("SCROLL_UP",   0.95),
        ("SCROLL_DOWN", 0.94),
        ("MOVE_RIGHT",  0.93),
        ("MOVE_RIGHT",  0.93),
        ("MOVE_LEFT",   0.92),
        ("MOVE_UP",     0.91),
        ("MOVE_DOWN",   0.90),
    ]
    for cmd, conf in commands:
        publish(cmd, conf)
        time.sleep(1.5)

def run_full_sequence():
    print("\n" + "=" * 55)
    print("  FULL AUTOMATION SEQUENCE VIA MQTT")
    print("=" * 55)
    run_calculator_sequence()
    time.sleep(2)
    run_notepad_sequence()
    time.sleep(2)
    run_browser_sequence()
    time.sleep(2)
    run_mouse_sequence()
    time.sleep(2)
    run_media_sequence()
    print("\n✅ Full sequence complete")

# ─── Interactive Menu ────────────────────────────────────────────────────────

def interactive_menu():
    print("\n" + "=" * 55)
    print("  SYNAPTIMESH — MQTT Publisher")
    print("=" * 55)
    print("  1. Send single command")
    print("  2. Run media sequence")
    print("  3. Run calculator sequence")
    print("  4. Run notepad sequence")
    print("  5. Run browser sequence")
    print("  6. Run mouse sequence")
    print("  7. Run FULL sequence")
    print("  0. Exit")
    print("=" * 55)

    while True:
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            cmd  = input("Command name (e.g. PLAY): ").strip().upper()
            conf = input("Confidence (default 0.95): ").strip()
            conf = float(conf) if conf else 0.95
            publish(cmd, conf)

        elif choice == "2":
            run_media_sequence()

        elif choice == "3":
            run_calculator_sequence()

        elif choice == "4":
            run_notepad_sequence()

        elif choice == "5":
            run_browser_sequence()

        elif choice == "6":
            run_mouse_sequence()

        elif choice == "7":
            run_full_sequence()

        elif choice == "0":
            print("Exiting publisher.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Direct command from terminal:
        # python -m app.mqtt_publisher PLAY 0.95
        cmd  = sys.argv[1].upper()
        conf = float(sys.argv[2]) if len(sys.argv) > 2 else 0.95
        publish(cmd, conf)
    else:
        interactive_menu()

publisher.loop_stop()
publisher.disconnect()