import json
import logging.config
import os
from pathlib import Path

from src import create_directories, add_logging_name
from src.config.environment import LOG_LEVEL
from src.application import Buache


def startup():
    directories = ['data/logs']
    create_directories(directories)

    levels = [
        {
            'num': logging.DEBUG - 9,
            'name': 'TRACE',
        },
        {
            'num': logging.DEBUG + 5,
            'name': 'VERBOSE',
        },
    ]

    for level in levels:
        add_logging_name(level)

    with open(Path("config/log.json").absolute(), "r", encoding="UTF8") as f:
        logger_config = json.load(f)

    logging.config.dictConfig(logger_config)
    logging.getLogger('startup').setLevel(LOG_LEVEL)
    logging.getLogger('startup').info(f"Logger started")

    app = Buache()
    app.start()


"""
Run startup procedures.
"""
if not os.getenv('STARTUP_COMPLETE'):
    startup()
