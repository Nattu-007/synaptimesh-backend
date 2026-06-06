# app/commands/calculator.py

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

def open_calculator():

    try:

        os_name = platform.system()

        logger.info(
            f"Opening calculator on {os_name}"
        )

        if os_name == "Windows":

            subprocess.Popen(
                ["calc.exe"]
            )

        elif os_name == "Darwin":

            subprocess.Popen(
                ["open", "-a", "Calculator"]
            )

        else:

            subprocess.Popen(
                ["gnome-calculator"]
            )

        time.sleep(2)

        return _success(
            "OPEN_CALCULATOR"
        )

    except Exception as e:

        return _failure(
            "OPEN_CALCULATOR",
            e
        )


def close_calculator():

    try:

        pyautogui.hotkey(
            "alt",
            "f4"
        )

        return _success(
            "CLOSE_CALCULATOR"
        )

    except Exception as e:

        return _failure(
            "CLOSE_CALCULATOR",
            e
        )


# =====================================================
# BASIC CONTROLS
# =====================================================

def calculator_clear():

    try:

        pyautogui.press(
            "escape"
        )

        return _success(
            "CALCULATOR_CLEAR"
        )

    except Exception as e:

        return _failure(
            "CALCULATOR_CLEAR",
            e
        )


def calculator_equals():

    try:

        pyautogui.press(
            "enter"
        )

        return _success(
            "CALCULATOR_EQUALS"
        )

    except Exception as e:

        return _failure(
            "CALCULATOR_EQUALS",
            e
        )


def calculator_backspace():

    try:

        pyautogui.press(
            "backspace"
        )

        return _success(
            "CALCULATOR_BACKSPACE"
        )

    except Exception as e:

        return _failure(
            "CALCULATOR_BACKSPACE",
            e
        )


def calculator_copy_result():

    try:

        pyautogui.hotkey(
            "ctrl",
            "c"
        )

        return _success(
            "CALCULATOR_COPY"
        )

    except Exception as e:

        return _failure(
            "CALCULATOR_COPY",
            e
        )


# =====================================================
# GENERIC CALCULATOR INPUT
# =====================================================

def calculate_expression(
    left,
    operator,
    right
):

    try:

        open_calculator()

        time.sleep(1)

        pyautogui.typewrite(
            str(left),
            interval=0.05
        )

        time.sleep(0.2)

        pyautogui.press(
            operator
        )

        time.sleep(0.2)

        pyautogui.typewrite(
            str(right),
            interval=0.05
        )

        time.sleep(0.2)

        pyautogui.press(
            "enter"
        )

        result_text = (
            f"{left} {operator} {right}"
        )

        logger.info(
            f"Calculator executed: "
            f"{result_text}"
        )

        return _success(
            "CALCULATOR_EXPRESSION",
            expression=result_text
        )

    except Exception as e:

        return _failure(
            "CALCULATOR_EXPRESSION",
            e
        )


# =====================================================
# PREDEFINED DEMOS
# =====================================================

def calculate_addition():

    try:

        close_calculator()

    except Exception:
        pass

    time.sleep(0.5)

    result = calculate_expression(
        3000,
        "add",
        457
    )

    logger.info(
        "3000 + 457 = 3457"
    )

    return result


def calculate_subtraction():

    try:

        close_calculator()

    except Exception:
        pass

    time.sleep(0.5)

    result = calculate_expression(
        3000,
        "subtract",
        457
    )

    logger.info(
        "3000 - 457 = 2543"
    )

    return result


# =====================================================
# FUTURE OPERATIONS
# =====================================================

def calculate_multiplication():

    return calculate_expression(
        3000,
        "multiply",
        457
    )


def calculate_division():

    return calculate_expression(
        3000,
        "divide",
        457
    )