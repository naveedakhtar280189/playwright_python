import logging

def get_logger(log_file='test_log.log'):
    """
    Creates and returns a logger that logs messages to a file.
    Ensures only one handler is added to prevent duplicate logs.

    :param log_file: Path to the log file.
    :return: Configured logger instance.
    """
    logger = logging.getLogger('automation_logger')
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

""" 
from logger_utils import get_logger

logger = get_logger()

logger.info("Test execution started.")
logger.debug("Opening browser.")
logger.error("Login button not found.")
logger.warning("Test ran longer than expected.") """