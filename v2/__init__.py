import os
from pathlib import Path

os.environ['ROOT'] = Path(__file__).absolute().parent.__str__()

import json
import logging.config
"""
Remember to add all new classes to __all__
"""

__all__ = [

]

# Define custom logging levels
new_levels = {
    'VERBOSE': 15,
    'DEBUG2': 5,
    'TRACE': 1
}

for name, level in new_levels.items():
    logging.addLevelName(level, name.upper())
    logging.addLevelName(level, name.lower())

    def function(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    setattr(logging.Logger, name.lower(), function)

try:
    config_folder = Path(f'{os.getenv("ROOT")}/config').absolute()
    config_folder.mkdir(exist_ok=True)

    config_file = Path(f'{os.getenv("ROOT")}/config/log.config').absolute()

    with open(f'{config_folder}', 'r') as log_config:
        logging.config.dictConfig(json.load(log_config))
except PermissionError as e:
    print(e)