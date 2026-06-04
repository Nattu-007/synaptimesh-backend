# app/commands/__init__.py
from app.commands.media import (
    play, pause, stop,
    volume_up, volume_down, mute,
    next_track, prev_track
)
from app.commands.browser import (
    open_browser, close_browser,
    new_tab, close_tab
)
from app.commands.mouse import (
    scroll_up, scroll_down,
    click, right_click,
    move_left, move_right
)

ACTION_MAP = {
    # Media
    "PLAY":          play,
    "PAUSE":         pause,
    "STOP":          stop,
    "VOLUME_UP":     volume_up,
    "VOLUME_DOWN":   volume_down,
    "MUTE":          mute,
    "NEXT_TRACK":    next_track,
    "PREV_TRACK":    prev_track,
    # Browser
    "OPEN_BROWSER":  open_browser,
    "CLOSE_BROWSER": close_browser,
    "NEW_TAB":       new_tab,
    "CLOSE_TAB":     close_tab,
    # Mouse
    "SCROLL_UP":     scroll_up,
    "SCROLL_DOWN":   scroll_down,
    "CLICK":         click,
    "RIGHT_CLICK":   right_click,
    "MOVE_LEFT":     move_left,
    "MOVE_RIGHT":    move_right,
}

def execute_command(command: str) -> str:
    action = ACTION_MAP.get(command)
    if action:
        try:
            action()
            return f"Executed: {command}"
        except Exception as e:
            return f"Execution error for {command}: {str(e)}"
    return f"No action mapped for: {command}"