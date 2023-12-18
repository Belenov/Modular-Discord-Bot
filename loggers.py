import logging
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(__name__)

action_logger = logging.getLogger(f"{__name__}_action")
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S%z"
)
handler = TimedRotatingFileHandler("actions.log", when="midnight")
handler.setFormatter(formatter)
action_logger.addHandler(handler)
