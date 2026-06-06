import webbrowser

from app.logger import get_logger

logger = get_logger(__name__)


def open_url(url: str):

    logger.info(
        f"Opening URL: {url}"
    )

    webbrowser.open(url)

    return {
        "status": "success",
        "url": url
    }


def open_google():

    return open_url(
        "https://www.google.com"
    )