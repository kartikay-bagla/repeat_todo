import logging
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

from repeat_todo.settings import ENV


def configure_logger(app):
    """Configure loggers."""
    logger = logging.getLogger("repeat_todo")
    json_handler = RotatingFileHandler(
        "repeat_todo.log", maxBytes=4194304, backupCount=5
    )
    json_formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s "
        "%(message)s %(lineno)s %(funcName)s %(filename)s"
    )
    json_handler.setFormatter(json_formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)

    log_level = logging.INFO if ENV == "production" else logging.DEBUG
    logger.setLevel(log_level)

    logger.addHandler(json_handler)
    logger.addHandler(stream_handler)

    if not app.logger.handlers:
        app.logger.addHandler(json_handler)
        app.logger.addHandler(stream_handler)
