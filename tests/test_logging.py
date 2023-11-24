import loguru

from lanarky.logging import get_logger


def test_get_logger_default():
    logger = get_logger()

    assert logger is not None
    assert isinstance(logger, loguru._logger.Logger)


def test_get_logger_custom_handler(tmpdir):
    custom_handler = tmpdir.join("test.log")
    logger = get_logger(handler=custom_handler, format="{time} - {message}")

    assert logger is not None
    assert isinstance(logger, loguru._logger.Logger)
    assert len(logger._core.handlers) == 1
    for handler in logger._core.handlers.values():
        assert handler._name == f"'{custom_handler}'"


def test_get_logger_kwargs(tmpdir):
    import logging

    custom_handler = tmpdir.join("test.log")
    level = logging.WARNING
    logger = get_logger(handler=custom_handler, level=level)

    assert logger is not None
    assert isinstance(logger, loguru._logger.Logger)
    assert len(logger._core.handlers) == 1
    for handler in logger._core.handlers.values():
        assert handler._name == f"'{custom_handler}'"
        assert handler._levelno == level
