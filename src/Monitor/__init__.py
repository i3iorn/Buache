from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.Adapters import BaseAdapter


class Monitor:
    def __init__(self, adapters: List['BaseAdapter']):
        self.adapters = adapters

    def adapters(self):
        file_adapters = [adapter for adapter in self.adapters if adapter.pre_load]