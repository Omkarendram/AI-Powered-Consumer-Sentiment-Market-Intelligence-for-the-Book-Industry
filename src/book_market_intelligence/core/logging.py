"""
Enterprise structured logging configuration.
"""

import logging
import sys
from typing import Optional

_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s:%(lineno)d | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "book_market_intelligence",
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configures and returns a structured logger instance.
    """
    logger = logging.getLogger(name)
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    # Avoid duplicate handlers if logger was already initialized
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setLevel(numeric_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except IOError as err:
                logger.warning(f"Could not initialize file handler at {log_file}: {err}")

    return logger


# Default application-wide logger
logger = setup_logger()
