import webbrowser

from app.logger import get_logger

logger = get_logger(__name__)


def open_gmail():

    url = (
        "https://mail.google.com"
    )

    logger.info(
        "Opening Gmail"
    )

    webbrowser.open(url)

    return {
        "status": "success",
        "url": url
    }