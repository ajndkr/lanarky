import sys
from typing import Any

import loguru


def get_logger(handler: Any = sys.stderr, **kwargs) -> loguru.Logger:
    logger = loguru.logger
    logger.remove()
    logger.add(handler, **kwargs)
    return logger


logger = get_logger()
