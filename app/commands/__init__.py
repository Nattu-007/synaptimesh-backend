# app/commands/__init__.py
import subprocess
import platform
import pyautogui

pyautogui.FAILSAFE = True

from app.commands.media   import (play, pause, stop, volume_up, volume_down,
                                   mute, next_track, prev_track)
from app.commands.browser import (open_browser, close_browser, new_tab,
                                   close_tab, browser_back, browser_forward,
                                   browser_refresh, browser_focus_address_bar)
from app.commands.mouse   import (scroll_up, scroll_down, scroll_up_fast,
                                   scroll_down_fast, click, right_click,
                                   move_left, move_right, move_up, move_down)
from app.commands.calculator import (open_calculator, close_calculator,
                                      calculator_clear, calculator_equals,
                                      calculator_backspace, calculator_copy_result,
                                      calculate_addition, calculate_subtraction)
from app.commands.notepad import (open_notepad, close_notepad, notepad_save,
                                   notepad_select_all, notepad_undo,
                                   notepad_new_file, notepad_copy, notepad_paste,
                                   notepad_full_automation)
from app.webapps.gmail import open_gmail
from app.webapps.netflix import open_netflix
ACTION_MAP = {
    # ── Media ──────────────────────────────────────────────────
    "PLAY":                      play,
    "PAUSE":                     pause,
    "STOP":                      stop,
    "VOLUME_UP":                 volume_up,
    "VOLUME_DOWN":               volume_down,
    "MUTE":                      mute,
    "NEXT_TRACK":                next_track,
    "PREV_TRACK":                prev_track,

    # ── Browser ────────────────────────────────────────────────
    "OPEN_BROWSER":              open_browser,
    "CLOSE_BROWSER":             close_browser,
    "NEW_TAB":                   new_tab,
    "CLOSE_TAB":                 close_tab,
    "BROWSER_BACK":              browser_back,
    "BROWSER_FORWARD":           browser_forward,
    "BROWSER_REFRESH":           browser_refresh,
    "BROWSER_FOCUS_ADDRESS_BAR": browser_focus_address_bar,


    # ── Mouse ──────────────────────────────────────────────────
    "MOVE_LEFT":                 move_left,
    "MOVE_RIGHT":                move_right,
    "MOVE_UP":                   move_up,
    "MOVE_DOWN":                 move_down,
    "CLICK":                     click,
    "RIGHT_CLICK":               right_click,

    # ── Scroll ─────────────────────────────────────────────────
    "SCROLL_UP":                 scroll_up,
    "SCROLL_DOWN":               scroll_down,
    "SCROLL_UP_FAST":            scroll_up_fast,
    "SCROLL_DOWN_FAST":          scroll_down_fast,

    # ── Calculator ─────────────────────────────────────────────
    "OPEN_CALCULATOR":           open_calculator,
    "CLOSE_CALCULATOR":          close_calculator,
    "CALCULATOR_CLEAR":          calculator_clear,
    "CALCULATOR_EQUALS":         calculator_equals,
    "CALCULATOR_BACKSPACE":      calculator_backspace,
    "CALCULATOR_COPY_RESULT":    calculator_copy_result,
    "CALCULATOR_ADD":            calculate_addition,      # ← NEW
    "CALCULATOR_SUBTRACT":       calculate_subtraction,   # ← NEW

    # ── Notepad ────────────────────────────────────────────────
    "OPEN_NOTEPAD":              open_notepad,
    "CLOSE_NOTEPAD":             close_notepad,
    "NOTEPAD_SAVE":              notepad_save,
    "NOTEPAD_SELECT_ALL":        notepad_select_all,
    "NOTEPAD_UNDO":              notepad_undo,
    "NOTEPAD_NEW_FILE":          notepad_new_file,
    "NOTEPAD_COPY":              notepad_copy,
    "NOTEPAD_PASTE":             notepad_paste,
    "NOTEPAD_FULL_AUTOMATION":   notepad_full_automation, # ← NEW
    "OPEN_GMAIL": open_gmail,
    "OPEN_NETFLIX": open_netflix,
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