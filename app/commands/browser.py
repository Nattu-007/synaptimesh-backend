# app/commands/browser.py

import platform
import subprocess
import webbrowser

import pyautogui

from app.logger import get_logger

logger = get_logger(__name__)

pyautogui.FAILSAFE = True

DEFAULT_URL = "https://www.google.com"


# =====================================================
# INTERNAL HELPERS
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
# OPEN URL
# =====================================================

def open_url(url: str):

    try:

        logger.info(
            f"Opening URL: {url}"
        )

        webbrowser.open(url)

        return _success(
            "OPEN_URL",
            url=url
        )

    except Exception as e:

        return _failure(
            "OPEN_URL",
            e
        )


# =====================================================
# OPEN BROWSER
# =====================================================

def open_browser(url=DEFAULT_URL):

    try:

        os_name = platform.system()

        logger.info(
            f"Opening browser on {os_name}"
        )

        if os_name == "Windows":

            try:

                subprocess.Popen(
                    ["start", "chrome", url],
                    shell=True
                )

            except Exception:

                webbrowser.open(url)

        elif os_name == "Darwin":

            subprocess.Popen(
                ["open", "-a", "Google Chrome", url]
            )

        else:

            subprocess.Popen(
                ["xdg-open", url]
            )

        return _success(
            "OPEN_BROWSER",
            url=url
        )

    except Exception as e:

        return _failure(
            "OPEN_BROWSER",
            e
        )


# =====================================================
# CLOSE BROWSER
# =====================================================

def close_browser():

    try:

        pyautogui.hotkey(
            "alt",
            "f4"
        )

        return _success(
            "CLOSE_BROWSER"
        )

    except Exception as e:

        return _failure(
            "CLOSE_BROWSER",
            e
        )


# =====================================================
# TABS
# =====================================================

def new_tab():

    try:

        pyautogui.hotkey(
            "ctrl",
            "t"
        )

        return _success(
            "NEW_TAB"
        )

    except Exception as e:

        return _failure(
            "NEW_TAB",
            e
        )


def close_tab():

    try:

        pyautogui.hotkey(
            "ctrl",
            "w"
        )

        return _success(
            "CLOSE_TAB"
        )

    except Exception as e:

        return _failure(
            "CLOSE_TAB",
            e
        )


# =====================================================
# NAVIGATION
# =====================================================

def browser_back():

    try:

        pyautogui.hotkey(
            "alt",
            "left"
        )

        return _success(
            "BROWSER_BACK"
        )

    except Exception as e:

        return _failure(
            "BROWSER_BACK",
            e
        )


def browser_forward():

    try:

        pyautogui.hotkey(
            "alt",
            "right"
        )

        return _success(
            "BROWSER_FORWARD"
        )

    except Exception as e:

        return _failure(
            "BROWSER_FORWARD",
            e
        )


def browser_refresh():

    try:

        pyautogui.press(
            "f5"
        )

        return _success(
            "BROWSER_REFRESH"
        )

    except Exception as e:

        return _failure(
            "BROWSER_REFRESH",
            e
        )


def browser_focus_address_bar():

    try:

        pyautogui.hotkey(
            "ctrl",
            "l"
        )

        return _success(
            "BROWSER_ADDRESS_BAR"
        )

    except Exception as e:

        return _failure(
            "BROWSER_ADDRESS_BAR",
            e
        )


# =====================================================
# WEB APPS
# =====================================================

def open_youtube():

    return open_url(
        "https://www.youtube.com"
    )


def open_gmail():

    return open_url(
        "https://mail.google.com"
    )


def open_netflix():

    return open_url(
        "https://www.netflix.com"
    )


def open_chatgpt():

    return open_url(
        "https://chatgpt.com"
    )


def open_google_drive():

    return open_url(
        "https://drive.google.com"
    )