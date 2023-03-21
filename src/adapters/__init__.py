import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api import Api


class BaseAdapter:
    def __init__(self, adapter):
        self.log = logging.getLogger(__name__)
        self.log.trace('Instantiating {}'.format(__name__))
        self.pre_load = adapter.config['type'] != 'api'

    @property
    def log(self) -> str:
        return self._log

    @log.setter
    def log(self, value: str) -> None:
        self._log = value

    @property
    def pre_load(self) -> str:
        return self._pre_load

    @pre_load.setter
    def pre_load(self, value: str) -> None:
        self._pre_load = value
