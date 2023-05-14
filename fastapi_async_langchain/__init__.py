import warnings

DEPRECATION_MESSAGE = """`fastapi_async_langchain` package name has been deprecated and will not receive any new updates.

For future releases, please install the `lanarky` package instead: `pip install lanarky`.
"""

warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)
