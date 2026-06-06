# app/mqtt_publisher.py

import json
import uuid
import time
import sys
import os

import paho.mqtt.client as mqtt

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.config import (
    MQTT_BROKER,
    MQTT_PORT
)

TOPIC = "synaptimesh/commands/desktop"

publisher = mqtt.Client(
    client_id="synaptimesh-publisher"
)

publisher.connect(
    MQTT_BROKER,
    MQTT_PORT
)

publisher.loop_start()

time.sleep(1)


# ==================================================
# Publish
# ==================================================

def publish(
    command: str,
    confidence: float = 0.95,
    category: str = "desktop",
    query: str | None = None
):

    message = {

        "correlation_id":
        str(uuid.uuid4())[:8],

        "command":
        command,

        "confidence":
        confidence,

        "source":
        "MQTT_TERMINAL",

        "timestamp":
        time.time(),

        "target":
        category
    }

    if query:
        message["query"] = query

    payload = json.dumps(
        message
    )

    result = publisher.publish(
        TOPIC,
        payload,
        qos=1
    )

    if result.rc == mqtt.MQTT_ERR_SUCCESS:

        print(
            f"[SENT] "
            f"{command}"
        )

        if query:

            print(
                f"       query={query}"
            )

    else:

        print(
            f"[FAILED] "
            f"{command}"
        )


# ==================================================
# WEB APP COMMANDS
# ==================================================

def youtube_play():

    query = input(
        "Video Search: "
    )

    publish(
        "PLAY_YOUTUBE_VIDEO",
        query=query
    )


def youtube_search():

    query = input(
        "Search Query: "
    )

    publish(
        "YOUTUBE_SEARCH",
        query=query
    )


def open_youtube():

    publish(
        "OPEN_YOUTUBE"
    )


def open_gmail():

    publish(
        "OPEN_GMAIL"
    )


def open_netflix():

    publish(
        "OPEN_NETFLIX"
    )


# ==================================================
# CHATBOT
# ==================================================

def chatbot_prompt():

    text = input(
        "Chat Prompt: "
    )

    publish(
        "CHATBOT",
        query=text,
        category="chatbot"
    )


# ==================================================
# MEDIA
# ==================================================

def run_media_sequence():

    commands = [

        ("PLAY", 0.95),

        ("VOLUME_UP", 0.94),

        ("VOLUME_UP", 0.94),

        ("NEXT_TRACK", 0.93),

        ("PREV_TRACK", 0.92),

        ("VOLUME_DOWN", 0.91),

        ("MUTE", 0.90),

        ("PAUSE", 0.89)
    ]

    for cmd, conf in commands:

        publish(
            cmd,
            conf
        )

        time.sleep(2)


# ==================================================
# CALCULATOR
# ==================================================

def run_calculator_sequence():

    publish(
        "OPEN_CALCULATOR"
    )

    time.sleep(3)

    publish(
        "CALCULATOR_ADD"
    )

    time.sleep(4)

    publish(
        "CALCULATOR_SUBTRACT"
    )

    time.sleep(4)

    publish(
        "CLOSE_CALCULATOR"
    )


# ==================================================
# NOTEPAD
# ==================================================

def run_notepad_sequence():

    publish(
        "OPEN_NOTEPAD"
    )

    time.sleep(3)

    publish(
        "NOTEPAD_FULL_AUTOMATION"
    )

    time.sleep(10)

    publish(
        "CLOSE_NOTEPAD"
    )


# ==================================================
# BROWSER
# ==================================================

def run_browser_sequence():

    publish(
        "OPEN_BROWSER"
    )

    time.sleep(4)

    publish(
        "NEW_TAB"
    )

    time.sleep(1)

    publish(
        "BROWSER_REFRESH"
    )

    time.sleep(1)

    publish(
        "BROWSER_BACK"
    )

    time.sleep(1)

    publish(
        "CLOSE_TAB"
    )

    time.sleep(1)

    publish(
        "CLOSE_BROWSER"
    )


# ==================================================
# FULL DEMO
# ==================================================

def run_full_sequence():

    print(
        "\nRunning full demo..."
    )

    run_calculator_sequence()

    time.sleep(2)

    run_notepad_sequence()

    time.sleep(2)

    run_browser_sequence()

    time.sleep(2)

    run_media_sequence()

    print(
        "\nDone."
    )


# ==================================================
# MENU
# ==================================================

def interactive_menu():

    while True:

        print("\n")

        print("=" * 60)

        print(
            "SYNAPTIMESH MQTT"
        )

        print("=" * 60)

        print("1  - Single Command")
        print("2  - Media Demo")
        print("3  - Calculator Demo")
        print("4  - Notepad Demo")
        print("5  - Browser Demo")
        print("6  - Full Demo")

        print()

        print("10 - Open Gmail")
        print("11 - Open Netflix")
        print("12 - Open YouTube")
        print("13 - Play YouTube Video")
        print("14 - Search YouTube")

        print()

        print("20 - Chatbot")

        print()

        print("0  - Exit")

        choice = input(
            "\nChoice: "
        ).strip()

        if choice == "1":

            cmd = input(
                "Command: "
            ).strip().upper()

            publish(cmd)

        elif choice == "2":

            run_media_sequence()

        elif choice == "3":

            run_calculator_sequence()

        elif choice == "4":

            run_notepad_sequence()

        elif choice == "5":

            run_browser_sequence()

        elif choice == "6":

            run_full_sequence()

        elif choice == "10":

            open_gmail()

        elif choice == "11":

            open_netflix()

        elif choice == "12":

            open_youtube()

        elif choice == "13":

            youtube_play()

        elif choice == "14":

            youtube_search()

        elif choice == "20":

            chatbot_prompt()

        elif choice == "0":

            break

        else:

            print(
                "Invalid option"
            )


# ==================================================
# ENTRY
# ==================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        command = (
            sys.argv[1]
            .upper()
        )

        query = None

        if len(sys.argv) > 2:

            query = (
                " ".join(
                    sys.argv[2:]
                )
            )

        publish(
            command,
            query=query
        )

    else:

        interactive_menu()

    publisher.loop_stop()

    publisher.disconnect()