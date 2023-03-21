import logging
from typing import List, TYPE_CHECKING

from src.queue import QueueItem

if TYPE_CHECKING:
    from src.adapters import BaseAdapter


class Monitor:
    def __init__(self, queue, adapters: List['BaseAdapter']):
        self.log = logging.getLogger(__name__)
        self.adapters = adapters
        self.queue = queue

        for adapter in [a for a in adapters if a.pre_load]:
            self.log.debug(f'Adding {adapter.__name__} to queue')
            qi = QueueItem(
                callback_class=adapter,
                callback_function_name='load'
            )
            self.log.debug(f'Queue item prepared {qi} for queue')
            self.queue.enqueue(qi)
        self.log.debug(f'Finnished monitor')
