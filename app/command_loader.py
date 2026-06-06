import json
import os

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "data", "emotiv_commands.json")

def load_commands() -> list:

    with open(
        COMMANDS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def get_verified_commands() -> list:

    return [
        c
        for c in load_commands()
        if c.get("status") == "verified"
    ]

def get_action_map() -> dict:

    return {
        c.get("desktop_action"): c
        for c in load_commands()
        if (
            c.get("status") == "verified"
            and c.get("desktop_action")
        )
    }

def get_confidence_map() -> dict:

    return {
        c.get("desktop_action"):
        c.get("confidence", 0.0)

        for c in load_commands()

        if (
            c.get("status") == "verified"
            and c.get("desktop_action")
        )
    }

def get_safety_map() -> dict:

    return {

        c.get("command"):
        c.get(
            "safety_guard",
            "none"
        )

        for c in load_commands()

        if c.get(
            "safety_guard",
            "none"
        ) != "none"
    }

def get_eeg_to_action_map() -> dict:

    return {

        (
            c.get("command"),
            c.get("category")
        ):
        c.get("desktop_action")

        for c in load_commands()

        if c.get("status") == "verified"
    }

def get_command_registry() -> set:

    return {

        c.get("desktop_action")

        for c in load_commands()

        if (
            c.get("status") == "verified"
            and c.get("desktop_action")
        )
    }

def get_rejected_commands() -> list:

    return [

        c

        for c in load_commands()

        if c.get("status") == "rejected"
    ]

ACTION_MAP = get_action_map()

CONFIDENCE_MAP = get_confidence_map()

SAFETY_MAP = get_safety_map()

EEG_TO_ACTION = get_eeg_to_action_map()

COMMAND_REGISTRY = get_command_registry()