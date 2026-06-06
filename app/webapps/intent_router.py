from app.logger import (
    get_logger
)

logger = get_logger(__name__)


def detect_intent(
    message: str
):

    text = (
        message
        .lower()
        .strip()
    )

    logger.info(
        f"Intent Detection: {text}"
    )

    # Gmail

    if (
        "open gmail" in text
        or "gmail" == text
    ):

        return {
            "action":
            "OPEN_GMAIL"
        }

    # Netflix

    if (
        "open netflix" in text
        or "netflix" == text
    ):

        return {
            "action":
            "OPEN_NETFLIX"
        }

    # YouTube

    if (
        "open youtube" in text
        or text == "youtube"
    ):

        return {
            "action":
            "OPEN_YOUTUBE"
        }

    # Play video

    if text.startswith(
        "play "
    ):

        query = text.replace(
            "play ",
            "",
            1
        )

        return {
            "action":
            "PLAY_YOUTUBE_VIDEO",

            "query":
            query
        }

    # Search YouTube

    if text.startswith(
        "search youtube "
    ):

        query = text.replace(
            "search youtube ",
            "",
            1
        )

        return {

            "action":
            "YOUTUBE_SEARCH",

            "query":
            query
        }

    # Suggestions

    if text.startswith(
        "suggest "
    ):

        query = text.replace(
            "suggest ",
            "",
            1
        )

        return {

            "action":
            "YOUTUBE_SUGGESTIONS",

            "query":
            query
        }

    return None