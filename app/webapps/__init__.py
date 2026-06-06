from .youtube import (
    open_youtube,
    search_videos,
    play_video,
    get_suggestions
)

from .gmail import open_gmail

from .netflix import open_netflix

from .chrome import (
    open_url,
    open_google
)

from .intent_router import detect_intent

__all__ = [
    "open_youtube",
    "search_videos",
    "play_video",
    "get_suggestions",
    "open_gmail",
    "open_netflix",
    "open_url",
    "open_google",
    "detect_intent"
]