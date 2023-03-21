import json
import logging.config
from pathlib import Path

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

with open(Path("Config/log.json").absolute(), "r", encoding="UTF8") as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)

logging.info(f"Logger started")
