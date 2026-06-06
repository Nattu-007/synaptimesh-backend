# app/logger.py
# Structured logging for Synaptimesh — daily rotation to logs/command_log.txt

import logging
import os
from logging.handlers import TimedRotatingFileHandler

LOG_DIR  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "command_log.txt")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT  = "%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger writing to console + logs/command_log.txt (daily rotation).

    Usage:
        from app.logger import get_logger
        logger = get_logger(__name__)
        logger.info("Command received: PLAY")
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # File — daily rotation, keep 7 days
    fh = TimedRotatingFileHandler(
        filename=LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    fh.suffix = "%Y-%m-%d"

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
