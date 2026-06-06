import webbrowser

from app.logger import get_logger

logger = get_logger(__name__)


def open_netflix():

    url = (
        "https://www.netflix.com"
    )

    logger.info(
        "Opening Netflix"
    )

    webbrowser.open(url)

    return {
        "status": "success",
        "url": url
    }