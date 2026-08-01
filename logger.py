import os
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_DIR, LOG_FILE, FILE_LOG_LEVEL, CONSOLE_LOG_LEVEL, MAX_LOG_SIZE_BYTES, BACKUP_COUNT, LOG_FORMAT, ROOT_LOGGER_NAME

_configured = False # per assicurarsi che venga configurato una volta sola

def _configure_root_logger():
    global _configured
    if _configured:
        return

    os.makedirs(LOG_DIR, exist_ok=True)

    root_logger = logging.getLogger(ROOT_LOGGER_NAME)
    root_logger.setLevel(logging.DEBUG)  # il filtro vero lo fanno gli handler

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_LOG_SIZE_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(FILE_LOG_LEVEL)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(CONSOLE_LOG_LEVEL)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _configured = True


def get_logger(name: str = None) -> logging.Logger:
    _configure_root_logger()

    if name is None or name == "__main__":
        return logging.getLogger(ROOT_LOGGER_NAME)

    return logging.getLogger(f"{ROOT_LOGGER_NAME}.{name}")