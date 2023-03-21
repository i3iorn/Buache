import logging

from src.Config.environment import LOG_LEVEL

logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

