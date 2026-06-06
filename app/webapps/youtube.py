import webbrowser

from youtubesearchpython import VideosSearch

from app.logger import get_logger

logger = get_logger(__name__)


def open_youtube():

    url = "https://www.youtube.com"

    logger.info(
        "Opening YouTube"
    )

    webbrowser.open(url)

    return {
        "status": "success",
        "url": url
    }


def search_videos(
    query: str,
    limit: int = 5
):

    logger.info(
        f"YouTube Search: {query}"
    )

    results = VideosSearch(
        query,
        limit=limit
    ).result()

    videos = []

    for item in results["result"]:

        videos.append({

            "title":
            item["title"],

            "channel":
            item["channel"]["name"],

            "duration":
            item.get("duration"),

            "views":
            item.get("viewCount", {})
            .get("text"),

            "url":
            f"https://youtube.com/watch?v={item['id']}"
        })

    return videos


def get_suggestions(
    query: str,
    limit: int = 5
):

    return search_videos(
        query=query,
        limit=limit
    )


def play_video(
    query: str
):

    videos = search_videos(
        query,
        limit=1
    )

    if not videos:

        logger.warning(
            f"No video found: {query}"
        )

        return None

    video = videos[0]

    logger.info(
        f"Playing: {video['title']}"
    )

    webbrowser.open(
        video["url"]
    )

    return video