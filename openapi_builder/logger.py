import logging

logger = logging.getLogger("openapi_builder")


def info(*args, **kwargs):
    return logger.info(*args, **kwargs)


def warning(*args, **kwargs):
    return logger.warning(*args, **kwargs)


def error(*args, **kwargs):
    return logger.error(*args, **kwargs)
