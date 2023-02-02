from loguru import logger as loguru_logger
import sys

def set_log_configurations():
    """
    set the log level by default info and determine colors and format log output
    """
    log_level = "INFO"
    logger = loguru_logger
    logger.remove()  # Default "sys.stderr" sink is not picklable

    logger.add(sys.stdout, colorize=True, format="<level>{time:YYYY-MM-DD HH:mm:ss} [{level}] {message}</level>",
               level=log_level)

    logger.level("CRITICAL", color="<red> <bold>")
    logger.level("ERROR", color="<red>")
    logger.level("WARNING", color="<yellow>")
    logger.level("INFO", color="<cyan> <bold>")
    logger.level("DEBUG", color="<green> <bold>")
    return logger

log = set_log_configurations()