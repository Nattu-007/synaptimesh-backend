# app/mqtt_runner.py
# Run this file to start the MQTT command listener
# It will execute desktop automation when messages arrive

import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.mqtt_client import client, connect
from app.config import MQTT_BROKER, MQTT_PORT

def start_listener():
    print("=" * 55)
    print("  SYNAPTIMESH — MQTT Command Listener")
    print("=" * 55)
    print(f"  Broker : {MQTT_BROKER}:{MQTT_PORT}")
    print(f"  Topics : synaptimesh/commands/#")
    print(f"  FAILSAFE: Move mouse to TOP-LEFT to abort")
    print("=" * 55)
    print("  Waiting for commands...\n")

    connect()

    try:
        while True:
            time.sleep(0.1)   # Keep alive
    except KeyboardInterrupt:
        print("\n[MQTT] Listener stopped by user")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    start_listener()