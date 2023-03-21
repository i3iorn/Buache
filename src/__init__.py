import importlib
import logging
import os
import tracemalloc
from time import time, sleep

from .exceptions import AdapterCountException, BuacheException, SetupError
from .config.environment import ADAPTERS, LOG_PATH, LOG_LEVEL
from .monitor import Monitor

logging.captureWarnings(True)


def add_logging_name(item):
    logging.addLevelName(item['num'], item['name'])

    def log_to_root(message, *args, **kwargs):
        logging.log(item['num'], message, *args, **kwargs)

    def log_function(self, message, *args, **kwargs):
        if self.isEnabledFor(item['num']):
            self._log(item['num'], message, args, **kwargs)

    setattr(logging, item['name'], item['num'])
    setattr(logging.getLoggerClass(), item['name'].lower(), log_function)
    setattr(logging, item['name'].lower(), log_to_root)


def create_directories(dirs):
    """
    Creates a list of directories recursively if they do not exist.
    :param dirs: A list of directory paths to create.
    """
    for directory in dirs:
        parent = os.path.pardir
        new_path = f'{parent}/{directory}'
        if not os.path.exists(new_path):
            os.makedirs(new_path)
