# app/router.py

ROUTING_TABLE = {
    # ── commands ───────────────────────────────────────
    "PLAY":                      "synaptimesh/commands/media",
    "PAUSE":                     "synaptimesh/commands/media",
    "STOP":                      "synaptimesh/commands/media",
    "VOLUME_UP":                 "synaptimesh/commands/media",
    "VOLUME_DOWN":               "synaptimesh/commands/media",
    "MUTE":                      "synaptimesh/commands/media",
    "NEXT_TRACK":                "synaptimesh/commands/media",
    "PREV_TRACK":                "synaptimesh/commands/media",
    "OPEN_BROWSER":              "synaptimesh/commands/browser",
    "CLOSE_BROWSER":             "synaptimesh/commands/browser",
    "NEW_TAB":                   "synaptimesh/commands/browser",
    "CLOSE_TAB":                 "synaptimesh/commands/browser",
    "BROWSER_BACK":              "synaptimesh/commands/browser",
    "BROWSER_FORWARD":           "synaptimesh/commands/browser",
    "BROWSER_REFRESH":           "synaptimesh/commands/browser",
    "BROWSER_FOCUS_ADDRESS_BAR": "synaptimesh/commands/browser",
    "MOVE_LEFT":                 "synaptimesh/commands/mouse",
    "MOVE_RIGHT":                "synaptimesh/commands/mouse",
    "MOVE_UP":                   "synaptimesh/commands/mouse",
    "MOVE_DOWN":                 "synaptimesh/commands/mouse",
    "CLICK":                     "synaptimesh/commands/mouse",
    "RIGHT_CLICK":               "synaptimesh/commands/mouse",
    "SCROLL_UP":                 "synaptimesh/commands/mouse",
    "SCROLL_DOWN":               "synaptimesh/commands/mouse",
    "SCROLL_UP_FAST":            "synaptimesh/commands/mouse",
    "SCROLL_DOWN_FAST":          "synaptimesh/commands/mouse",
    "OPEN_CALCULATOR":           "synaptimesh/commands/calculator",
    "CLOSE_CALCULATOR":          "synaptimesh/commands/calculator",
    "CALCULATOR_CLEAR":          "synaptimesh/commands/calculator",
    "CALCULATOR_EQUALS":         "synaptimesh/commands/calculator",
    "CALCULATOR_BACKSPACE":      "synaptimesh/commands/calculator",
    "CALCULATOR_COPY_RESULT":    "synaptimesh/commands/calculator",
    "CALCULATOR_ADD":            "synaptimesh/commands/calculator",
    "CALCULATOR_SUBTRACT":       "synaptimesh/commands/calculator",
    "OPEN_NOTEPAD":              "synaptimesh/commands/notepad",
    "CLOSE_NOTEPAD":             "synaptimesh/commands/notepad",
    "NOTEPAD_SAVE":              "synaptimesh/commands/notepad",
    "NOTEPAD_SELECT_ALL":        "synaptimesh/commands/notepad",
    "NOTEPAD_UNDO":              "synaptimesh/commands/notepad",
    "NOTEPAD_NEW_FILE":          "synaptimesh/commands/notepad",
    "NOTEPAD_COPY":              "synaptimesh/commands/notepad",
    "NOTEPAD_PASTE":             "synaptimesh/commands/notepad",
    "NOTEPAD_FULL_AUTOMATION":   "synaptimesh/commands/notepad",
}

def get_topic(command: str) -> str:
    """
    Returns the MQTT topic for a given command.
    Returns None if the command is not in the routing table.
    """
    return ROUTING_TABLE.get(command)