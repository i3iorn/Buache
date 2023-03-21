import logging
import threading
from time import time
from typing import List

from src.config.environment import QUEUE_MAX_SIZE
from src.exceptions import AddToQueueError


class QueueItem:
    def __init__(self,
                 callback_module_name: str = None,
                 callback_module=None,
                 callback_class_name: str = None,
                 callback_class=None,
                 callback_function_name: str = None,
                 callback_function=None,
                 parameters: dict = None,
                 caller_name: str = None,
                 **kwargs
                 ):
        if callback_module is not None or callback_module_name is not None:
            self.callback_module = callback_module or __import__(callback_module_name)
        if callback_class is not None or callback_class_name is not None:
            self.callback_class = callback_class or getattr(self.callback_module, callback_class_name)
        self.callback_function = callback_function or getattr(self.callback_class, callback_function_name)

        self.parameters = parameters
        self.kwargs = kwargs
        self.caller = caller_name
        self.created = time()

    def __lt__(self, second, sort_by=None):
        sort_by = sort_by or 'create'
        if not getattr(self, sort_by):
            sort_by = 'create'
        first_attr = getattr(self, sort_by)
        second_attr = getattr(second, sort_by)
        return first_attr < second_attr


class Queue:
    def __init__(self, max_size=None, logger=None):
        self.items = []
        self.max_size = max_size or QUEUE_MAX_SIZE
        self.logger = logger or logging.getLogger(__name__)
        self.lock = threading.Lock()

    def __len__(self):
        with self.lock:
            return len(self.items)

    def clear(self):
        with self.lock:
            self.items.clear()
            self.logger.info('Queue cleared')

    def contains(self, item: QueueItem) -> bool:
        with self.lock:
            return item in self.items

    def dequeue(self, max_attempts=1) -> QueueItem:
        try_count = 0
        while try_count < max_attempts:
            self.logger.debug(f'Starting dequeing.')
            self.logger.debug(f'Lock status: {self.lock}')
            try:
                if self.empty():
                    raise ValueError('Queue is empty')
                with self.lock:
                    self.logger.debug(f'Lock status: {self.lock}')

                    item = self.items.pop(0)
                    self.logger.info(f'Dequeued item {item}')
                    return item
            except Exception as e:
                self.logger.error(f'Error dequeuing item: {e}', exc_info=True)
                try_count += 1
        raise ValueError(f'Exceeded maximum attempts ({max_attempts}) to dequeue item')

    def empty(self):
        with self.lock:
            return len(self.items) == 0

    def enqueue(self, item: QueueItem) -> None:
        self.logger.debug(f'Status of lock is: {self.lock}')
        try:
            if self.max_size is not None and len(self) >= self.max_size:
                raise ValueError('Queue is full')
            with self.lock:
                self.logger.debug(f'Status of lock is: {self.lock}')
                self.items.append(item)
                self.logger.info(f'Enqueued item {item}')
        except Exception as e:
            self.logger.error(f'Error enqueuing item {item}: {e}', exc_info=True)
            raise AddToQueueError from e

    def first(self) -> QueueItem:
        try:
            if self.empty():
                raise ValueError('Queue is empty')
            with self.lock:
                item = self.items[0]
                self.logger.info(f'Front item is {item}')
                return item
        except Exception as e:
            self.logger.error(f'Error getting front item: {e}', exc_info=True)

    def get_items(self) -> List[QueueItem]:
        with self.lock:
            return self.items.copy()

    def last(self) -> QueueItem:
        try:
            if self.empty():
                raise ValueError('Queue is empty')
            with self.lock:
                item = self.items[-1]
                self.logger.info(f'Rear item is {item}')
                return item
        except Exception as e:
            self.logger.error(f'Error getting rear item: {e}', exc_info=True)

    def remove(self, item: QueueItem) -> None:
        try:
            if self.empty():
                raise ValueError('Queue is empty')
            with self.lock:
                self.items.remove(item)
                self.logger.info(f'Removed item {item}')
        except Exception as e:
            self.logger.error(f'Error removing item {item}: {e}', exc_info=True)

    def sort(self):
        try:
            with self.lock:
                self.items.sort()
                self.logger.info('Queue sorted')
        except Exception as e:
            self.logger.error(f'Error sorting queue: {e}', exc_info=True)
