# app/command_loader.py
import json
import os

COMMANDS_FILE = os.path.join(os.path.dirname(__file__), "data", "emotiv_commands.json")

def load_commands() -> list:
    with open(COMMANDS_FILE, "r") as f:
        return json.load(f)

def get_verified_commands() -> list:
    return [c for c in load_commands() if c["status"] == "verified"]

def get_action_map() -> dict:
    """
    { "PREV_TRACK": { full command entry }, ... }
    Keyed by desktop_action — used by dispatcher.
    """
    return {
        c["desktop_action"]: c
        for c in load_commands()
        if c["status"] == "verified"
    }

def get_confidence_map() -> dict:
    """
    { "PREV_TRACK": 0.9159, "NEXT_TRACK": 0.9241, ... }
    Per-command confidence from real sample data.
    """
    return {
        c["desktop_action"]: c["confidence"]
        for c in load_commands()
        if c["status"] == "verified"
    }

def get_safety_map() -> dict:
    """
    { "CLOSE_BROWSER": "focus_check", "CLICK": "failsafe_enabled", ... }
    """
    return {
        c["desktop_action"]: c["safety_guard"]
        for c in load_commands()
        if c["safety_guard"] != "none"
    }

def get_eeg_to_action_map() -> dict:
    """
    Maps raw EEG signal + category to desktop_action.
    { ("LEFT_HAND", "media"): "PREV_TRACK", ... }
    """
    return {
        (c["command"], c["category"]): c["desktop_action"]
        for c in load_commands()
        if c["status"] == "verified"
    }

def get_command_registry() -> set:
    """All valid desktop_action names — used by dispatcher."""
    return {
        c["desktop_action"]
        for c in load_commands()
        if c["status"] == "verified"
    }

def get_rejected_commands() -> list:
    """
    Return all commands marked as rejected.
    """
    return [
        c
        for c in load_commands()
        if c["status"] == "rejected"
    ]

# Pre-load everything on import
ACTION_MAP       = get_action_map()
CONFIDENCE_MAP   = get_confidence_map()
SAFETY_MAP       = get_safety_map()
EEG_TO_ACTION    = get_eeg_to_action_map()
COMMAND_REGISTRY = get_command_registry()