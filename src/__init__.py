import configparser
import os
import json
import logging.config
from pathlib import Path

from src.app import Application
from src.exceptions import ConfigurationError

os.environ['ROOT'] = Path(__file__).absolute().parent.__str__()

"""
Remember to add all new classes to __all__
"""

__all__ = [
    'Application',
    'run'
]

# Define custom logging levels
new_levels = {
    'VERBOSE': 15,
    'DEBUGX': 5,
    'TRACE': 1
}

for name, level in new_levels.items():
    logging.addLevelName(level, name.upper())


    def function(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    setattr(logging, name.upper(), level)
    setattr(logging.Logger, name.lower(), function)

config_folder = Path(f'{os.getenv("ROOT")}/config').absolute()
config_folder.mkdir(exist_ok=True)
country_folder = Path(f'{config_folder}/countries').absolute()
country_folder.mkdir(exist_ok=True)

log_config_file = Path(f'{config_folder}/log.json').absolute()

with open(f'{log_config_file}', 'r') as log_config:
    logging.config.dictConfig(json.load(log_config))

logger = logging.getLogger()
logger.setLevel('DEBUG')
logger.debug(f'Logging set up with additional levels, VERBOSE(15), DEBUGX(5), TRACE(1).')

logger.debug(f'Running main config file.')
main_config_file = Path(f'{config_folder}/config.ini').absolute()

try:
    config = configparser.ConfigParser()
    config.read(main_config_file.absolute())
    logger.debug(f'Configuration is loaded.')
except FileNotFoundError as e:
    msg = f'Could not read {main_config_file}'
    logger.error(msg)
    raise ConfigurationError(msg)

def run(**kwargs) -> Application:
    return Application(**kwargs)
