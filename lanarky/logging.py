import sys
from typing import Any

import loguru


def get_logger(handler: Any = sys.stderr, **kwargs: dict[str, Any]) -> Any:
    """Get a logger instance.

    Lanarky uses `loguru` for logging.

    Args:
        handler: The handler to use for the logger.

    Returns:
        A loguru logger instance.
    """
    logger = loguru.logger
    logger.remove()
    logger.add(handler, **kwargs)
    return logger


logger = get_logger()
