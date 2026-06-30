import logging
import sys
from logging.handlers import RotatingFileHandler

from grn_td.paths import RESULTS_DIR

LOG_FILE = RESULTS_DIR / "app.log"


def setup_logger():
    """Configure a root logger that works reliably across all files."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text("", encoding="utf-8")

    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(LOG_FILE, mode='a')

    logger = logging.getLogger()  #  Get the root logger

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        mode='a',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Keep propagation ON for root logger
    logger.propagate = True

    return logger


#  Initialize immediately when module loads
logger = setup_logger()