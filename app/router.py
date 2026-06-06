# app/router.py

ROUTING_TABLE = {
    # ── Desktop commands ───────────────────────────────────────
    "PLAY":                      "synaptimesh/commands/desktop",
    "PAUSE":                     "synaptimesh/commands/desktop",
    "STOP":                      "synaptimesh/commands/desktop",
    "VOLUME_UP":                 "synaptimesh/commands/desktop",
    "VOLUME_DOWN":               "synaptimesh/commands/desktop",
    "MUTE":                      "synaptimesh/commands/desktop",
    "NEXT_TRACK":                "synaptimesh/commands/desktop",
    "PREV_TRACK":                "synaptimesh/commands/desktop",
    "OPEN_BROWSER":              "synaptimesh/commands/desktop",
    "CLOSE_BROWSER":             "synaptimesh/commands/desktop",
    "NEW_TAB":                   "synaptimesh/commands/desktop",
    "CLOSE_TAB":                 "synaptimesh/commands/desktop",
    "BROWSER_BACK":              "synaptimesh/commands/desktop",
    "BROWSER_FORWARD":           "synaptimesh/commands/desktop",
    "BROWSER_REFRESH":           "synaptimesh/commands/desktop",
    "BROWSER_FOCUS_ADDRESS_BAR": "synaptimesh/commands/desktop",
    "MOVE_LEFT":                 "synaptimesh/commands/desktop",
    "MOVE_RIGHT":                "synaptimesh/commands/desktop",
    "MOVE_UP":                   "synaptimesh/commands/desktop",
    "MOVE_DOWN":                 "synaptimesh/commands/desktop",
    "CLICK":                     "synaptimesh/commands/desktop",
    "RIGHT_CLICK":               "synaptimesh/commands/desktop",
    "SCROLL_UP":                 "synaptimesh/commands/desktop",
    "SCROLL_DOWN":               "synaptimesh/commands/desktop",
    "SCROLL_UP_FAST":            "synaptimesh/commands/desktop",
    "SCROLL_DOWN_FAST":          "synaptimesh/commands/desktop",
    "OPEN_CALCULATOR":           "synaptimesh/commands/desktop",
    "CLOSE_CALCULATOR":          "synaptimesh/commands/desktop",
    "CALCULATOR_CLEAR":          "synaptimesh/commands/desktop",
    "CALCULATOR_EQUALS":         "synaptimesh/commands/desktop",
    "CALCULATOR_BACKSPACE":      "synaptimesh/commands/desktop",
    "CALCULATOR_COPY_RESULT":    "synaptimesh/commands/desktop",
    "CALCULATOR_ADD":            "synaptimesh/commands/desktop",
    "CALCULATOR_SUBTRACT":       "synaptimesh/commands/desktop",
    "OPEN_NOTEPAD":              "synaptimesh/commands/desktop",
    "CLOSE_NOTEPAD":             "synaptimesh/commands/desktop",
    "NOTEPAD_SAVE":              "synaptimesh/commands/desktop",
    "NOTEPAD_SELECT_ALL":        "synaptimesh/commands/desktop",
    "NOTEPAD_UNDO":              "synaptimesh/commands/desktop",
    "NOTEPAD_NEW_FILE":          "synaptimesh/commands/desktop",
    "NOTEPAD_COPY":              "synaptimesh/commands/desktop",
    "NOTEPAD_PASTE":             "synaptimesh/commands/desktop",
    "NOTEPAD_FULL_AUTOMATION":   "synaptimesh/commands/desktop",
}

def get_topic(command: str) -> str:
    """
    Returns the MQTT topic for a given command.
    Returns None if the command is not in the routing table.
    """
    return ROUTING_TABLE.get(command)