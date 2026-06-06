# app/commands/media.py

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


def _press(action, key):

    try:

        logger.info(
            f"{action} -> {key}"
        )

        pyautogui.press(key)

        return _success(action)

    except Exception as e:

        return _failure(
            action,
            e
        )


# =====================================================
# PLAYBACK
# =====================================================

def play():

    return _press(
        "PLAY",
        "playpause"
    )


def pause():

    return _press(
        "PAUSE",
        "playpause"
    )


def stop():

    return _press(
        "STOP",
        "stop"
    )


# =====================================================
# VOLUME
# =====================================================

def volume_up():

    return _press(
        "VOLUME_UP",
        "volumeup"
    )


def volume_down():

    return _press(
        "VOLUME_DOWN",
        "volumedown"
    )


def mute():

    return _press(
        "MUTE",
        "volumemute"
    )


# =====================================================
# TRACK CONTROL
# =====================================================

def next_track():

    return _press(
        "NEXT_TRACK",
        "nexttrack"
    )


def prev_track():

    return _press(
        "PREV_TRACK",
        "prevtrack"
    )


# =====================================================
# ADVANCED VOLUME CONTROL
# =====================================================

def volume_up_multiple(
    steps: int = 5
):

    try:

        for _ in range(steps):

            pyautogui.press(
                "volumeup"
            )

        logger.info(
            f"Volume increased by {steps}"
        )

        return _success(
            "VOLUME_UP_MULTIPLE",
            steps=steps
        )

    except Exception as e:

        return _failure(
            "VOLUME_UP_MULTIPLE",
            e
        )


def volume_down_multiple(
    steps: int = 5
):

    try:

        for _ in range(steps):

            pyautogui.press(
                "volumedown"
            )

        logger.info(
            f"Volume decreased by {steps}"
        )

        return _success(
            "VOLUME_DOWN_MULTIPLE",
            steps=steps
        )

    except Exception as e:

        return _failure(
            "VOLUME_DOWN_MULTIPLE",
            e
        )


# =====================================================
# FUTURE MEDIA INTEGRATIONS
# =====================================================

def spotify_play_pause():

    logger.info(
        "Spotify play/pause"
    )

    return play()


def youtube_music_play_pause():

    logger.info(
        "YouTube Music play/pause"
    )

    return play()


def vlc_play_pause():

    logger.info(
        "VLC play/pause"
    )

    return play()