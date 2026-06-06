# app/commands/notepad.py

import platform
import subprocess
import time

import pyautogui

from app.logger import get_logger

logger = get_logger(__name__)

pyautogui.FAILSAFE = True


# =====================================================
# HELPERS
# =====================================================

def _success(action, **extra):

    result = {
        "status": "success",
        "action": action
    }

    result.update(extra)

    return result


def _failure(action, error):

    logger.error(
        f"{action} failed: {error}"
    )

    return {
        "status": "error",
        "action": action,
        "error": str(error)
    }


# =====================================================
# OPEN / CLOSE
# =====================================================

def open_notepad():

    try:

        os_name = platform.system()

        logger.info(
            f"Opening notepad on {os_name}"
        )

        if os_name == "Windows":

            subprocess.Popen(
                ["notepad.exe"]
            )

        elif os_name == "Darwin":

            subprocess.Popen(
                ["open", "-a", "TextEdit"]
            )

        else:

            subprocess.Popen(
                ["gedit"]
            )

        time.sleep(2)

        return _success(
            "OPEN_NOTEPAD"
        )

    except Exception as e:

        return _failure(
            "OPEN_NOTEPAD",
            e
        )


def close_notepad():

    try:

        pyautogui.hotkey(
            "alt",
            "f4"
        )

        time.sleep(0.5)

        # Windows Notepad save prompt
        pyautogui.press("tab")
        pyautogui.press("enter")

        return _success(
            "CLOSE_NOTEPAD"
        )

    except Exception as e:

        return _failure(
            "CLOSE_NOTEPAD",
            e
        )


# =====================================================
# EDIT COMMANDS
# =====================================================

def notepad_save():

    try:

        pyautogui.hotkey(
            "ctrl",
            "s"
        )

        return _success(
            "NOTEPAD_SAVE"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_SAVE",
            e
        )


def notepad_select_all():

    try:

        pyautogui.hotkey(
            "ctrl",
            "a"
        )

        return _success(
            "NOTEPAD_SELECT_ALL"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_SELECT_ALL",
            e
        )


def notepad_undo():

    try:

        pyautogui.hotkey(
            "ctrl",
            "z"
        )

        return _success(
            "NOTEPAD_UNDO"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_UNDO",
            e
        )


def notepad_new_file():

    try:

        pyautogui.hotkey(
            "ctrl",
            "n"
        )

        return _success(
            "NOTEPAD_NEW_FILE"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_NEW_FILE",
            e
        )


def notepad_copy():

    try:

        pyautogui.hotkey(
            "ctrl",
            "c"
        )

        return _success(
            "NOTEPAD_COPY"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_COPY",
            e
        )


def notepad_paste():

    try:

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        return _success(
            "NOTEPAD_PASTE"
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_PASTE",
            e
        )


# =====================================================
# WRITE TEXT
# =====================================================

def write_text(
    text: str,
    interval: float = 0.03
):

    try:

        pyautogui.typewrite(
            text,
            interval=interval
        )

        return _success(
            "WRITE_TEXT",
            length=len(text)
        )

    except Exception as e:

        return _failure(
            "WRITE_TEXT",
            e
        )


# =====================================================
# SAVE FILE
# =====================================================

def save_file(
    filename="synaptimesh_automation_log"
):

    try:

        pyautogui.hotkey(
            "ctrl",
            "s"
        )

        time.sleep(1)

        pyautogui.typewrite(
            filename,
            interval=0.05
        )

        time.sleep(0.5)

        pyautogui.press(
            "enter"
        )

        logger.info(
            f"Saved file: {filename}"
        )

        return _success(
            "SAVE_FILE",
            filename=filename
        )

    except Exception as e:

        return _failure(
            "SAVE_FILE",
            e
        )


# =====================================================
# FULL AUTOMATION DEMO
# =====================================================

def notepad_full_automation():

    try:

        open_notepad()

        time.sleep(1)

        lines = [

            "========================================",
            "  SYNAPTIMESH — Desktop Automation Log  ",
            "========================================",

            "",

            "Session   : EEG-Controlled Automation",
            "Headset   : Emotiv EPOC X",
            "Backend   : SynaptiMesh FastAPI Server",

            "",

            "Commands Executed:",

            "  [1] OPEN_NOTEPAD",
            "  [2] NOTEPAD_SELECT_ALL",
            "  [3] NOTEPAD_COPY",
            "  [4] NOTEPAD_SAVE",
            "  [5] OPEN_CALCULATOR",
            "  [6] Addition 3000 + 457 = 3457",
            "  [7] Subtraction 3000 - 457 = 2543",
            "  [8] CLOSE_CALCULATOR",

            "",

            "========================================",
            "         Automation is done             ",
            "========================================",
        ]

        for line in lines:

            pyautogui.typewrite(
                line,
                interval=0.03
            )

            pyautogui.press(
                "enter"
            )

            time.sleep(0.1)

        save_file(
            "synaptimesh_automation_log"
        )

        logger.info(
            "Notepad automation completed"
        )

        return _success(
            "NOTEPAD_FULL_AUTOMATION",
            lines_written=len(lines)
        )

    except Exception as e:

        return _failure(
            "NOTEPAD_FULL_AUTOMATION",
            e
        )