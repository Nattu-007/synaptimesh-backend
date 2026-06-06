# app/commands/mouse.py

import pyautogui

from app.logger import get_logger

logger = get_logger(__name__)

pyautogui.FAILSAFE = True


SCROLL_AMOUNT = 500
SCROLL_AMOUNT_FAST = 1500

MOVE_DISTANCE = 250


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


def _current_position():

    x, y = pyautogui.position()

    return x, y


def _screen_size():

    return pyautogui.size()


# =====================================================
# SCROLLING
# =====================================================

def scroll_up():

    try:

        pyautogui.scroll(
            SCROLL_AMOUNT
        )

        return _success(
            "SCROLL_UP",
            amount=SCROLL_AMOUNT
        )

    except Exception as e:

        return _failure(
            "SCROLL_UP",
            e
        )


def scroll_down():

    try:

        pyautogui.scroll(
            -SCROLL_AMOUNT
        )

        return _success(
            "SCROLL_DOWN",
            amount=SCROLL_AMOUNT
        )

    except Exception as e:

        return _failure(
            "SCROLL_DOWN",
            e
        )


def scroll_up_fast():

    try:

        pyautogui.scroll(
            SCROLL_AMOUNT_FAST
        )

        return _success(
            "SCROLL_UP_FAST",
            amount=SCROLL_AMOUNT_FAST
        )

    except Exception as e:

        return _failure(
            "SCROLL_UP_FAST",
            e
        )


def scroll_down_fast():

    try:

        pyautogui.scroll(
            -SCROLL_AMOUNT_FAST
        )

        return _success(
            "SCROLL_DOWN_FAST",
            amount=SCROLL_AMOUNT_FAST
        )

    except Exception as e:

        return _failure(
            "SCROLL_DOWN_FAST",
            e
        )


# =====================================================
# CLICK ACTIONS
# =====================================================

def click():

    try:

        pyautogui.click()

        x, y = _current_position()

        return _success(
            "CLICK",
            x=x,
            y=y
        )

    except Exception as e:

        return _failure(
            "CLICK",
            e
        )


def double_click():

    try:

        pyautogui.doubleClick()

        x, y = _current_position()

        return _success(
            "DOUBLE_CLICK",
            x=x,
            y=y
        )

    except Exception as e:

        return _failure(
            "DOUBLE_CLICK",
            e
        )


def right_click():

    try:

        pyautogui.rightClick()

        x, y = _current_position()

        return _success(
            "RIGHT_CLICK",
            x=x,
            y=y
        )

    except Exception as e:

        return _failure(
            "RIGHT_CLICK",
            e
        )


# =====================================================
# CURSOR MOVEMENT
# =====================================================

def move_left(px: int = MOVE_DISTANCE):

    try:

        x, y = _current_position()

        new_x = max(
            0,
            x - px
        )

        pyautogui.moveTo(
            new_x,
            y,
            duration=0.2
        )

        return _success(
            "MOVE_LEFT",
            x=new_x,
            y=y
        )

    except Exception as e:

        return _failure(
            "MOVE_LEFT",
            e
        )


def move_right(px: int = MOVE_DISTANCE):

    try:

        x, y = _current_position()

        screen_w, _ = _screen_size()

        new_x = min(
            screen_w - 1,
            x + px
        )

        pyautogui.moveTo(
            new_x,
            y,
            duration=0.2
        )

        return _success(
            "MOVE_RIGHT",
            x=new_x,
            y=y
        )

    except Exception as e:

        return _failure(
            "MOVE_RIGHT",
            e
        )


def move_up(px: int = MOVE_DISTANCE):

    try:

        x, y = _current_position()

        new_y = max(
            0,
            y - px
        )

        pyautogui.moveTo(
            x,
            new_y,
            duration=0.2
        )

        return _success(
            "MOVE_UP",
            x=x,
            y=new_y
        )

    except Exception as e:

        return _failure(
            "MOVE_UP",
            e
        )


def move_down(px: int = MOVE_DISTANCE):

    try:

        x, y = _current_position()

        _, screen_h = _screen_size()

        new_y = min(
            screen_h - 1,
            y + px
        )

        pyautogui.moveTo(
            x,
            new_y,
            duration=0.2
        )

        return _success(
            "MOVE_DOWN",
            x=x,
            y=new_y
        )

    except Exception as e:

        return _failure(
            "MOVE_DOWN",
            e
        )


# =====================================================
# FUTURE GESTURES
# =====================================================

def drag_left(px: int = 300):

    try:

        pyautogui.dragRel(
            -px,
            0,
            duration=0.5
        )

        return _success(
            "DRAG_LEFT",
            pixels=px
        )

    except Exception as e:

        return _failure(
            "DRAG_LEFT",
            e
        )


def drag_right(px: int = 300):

    try:

        pyautogui.dragRel(
            px,
            0,
            duration=0.5
        )

        return _success(
            "DRAG_RIGHT",
            pixels=px
        )

    except Exception as e:

        return _failure(
            "DRAG_RIGHT",
            e
        )