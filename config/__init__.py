from json import load as json_load
from logging import Logger, getLogger, addLevelName, config as logging_config
from configparser import ConfigParser
from pathlib import Path

from src.exceptions import ConfigurationError

ROOT = Path(__file__).absolute().parent.parent.__str__()

# Define custom logging levels
new_levels = {
    'VERBOSE': 15,
    'DEBUGX': 5,
    'TRACE': 1
}


for name, level in new_levels.items():
    addLevelName(level, name.upper())


    def function(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    setattr(__import__('logging'), name.upper(), level)
    setattr(Logger, name.lower(), function)

config_folder = Path(f'{ROOT}/config').absolute()
config_folder.mkdir(exist_ok=True)
country_folder = Path(f'{config_folder}/countries').absolute()
country_folder.mkdir(exist_ok=True)

log_config_file = Path(f'{config_folder}/log.json').absolute()

with open(f'{log_config_file}', 'r') as log_config:
    print(log_config_file)
    logging_config.dictConfig(json_load(log_config))

logger = getLogger()
logger.setLevel('DEBUG')
logger.debug(f'Logging set up with additional levels, VERBOSE(15), DEBUGX(5), TRACE(1).')

logger.debug(f'Running main config file.')

main_config_file = Path(f'{config_folder}/config.ini').absolute()
heuristics_config_file = Path(f'{config_folder}/heuristics.ini').absolute()

try:
    CONFIG = ConfigParser()
    CONFIG.read(main_config_file)
    CONFIG.read(heuristics_config_file)

except FileNotFoundError as e:
    msg = f'Could not read {main_config_file}'
    logger.error(msg)
    raise ConfigurationError(msg)
