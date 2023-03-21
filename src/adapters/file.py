import pickle
from pathlib import Path

from src.adapters import BaseAdapter
from src.config.environment import ROOT_DIR


class File(BaseAdapter):
    def __init__(self, config: dict, path: str = None):
        """
        Initialize the File object.
        :param config: Adapter config dict
        :param path: The path of the file.
        """
        self.config = config or {}
        super().__init__(self)
        self.log.trace(f'Instantiating {__name__}')
        self.path = path or config['path'] or ''
        self.path = Path(f'{ROOT_DIR}/{self.path}')

        self.name = self.config['name']

    def __name__(self):
        return self.config['name']

    def load(self):
        try:
            with open(self.path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None

    def save(self, data):
        with open(self.path, 'wb') as file:
            pickle.dump(data, file)
