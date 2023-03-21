import logging


class QueueItem:
    def __init__(self,
                 callback_module_name: str,
                 callback_class_name: str,
                 parameters: dict,
                 caller_name: str,
                 **kwargs
                 ):
        self.callback_module_name = callback_module_name
        self.callback_class_name = callback_class_name
        self.parameters = parameters
        self.kwargs = kwargs
        self.caller = caller_name


class Queue:
    def __init__(self):
        self.items = []
        self.logger = logging.getLogger('Queue')

    def enqueue(self, item: QueueItem) -> None:
        try:
            self.items.append(item)
            self.logger.info(f'Enqueued item {item}')
        except Exception as e:
            self.logger.error(f'Error enqueuing item {item}: {e}')

    def dequeue(self) -> QueueItem:
        try:
            if self.is_empty():
                raise ValueError('Queue is empty')
            item = self.items.pop(0)
            self.logger.info(f'Dequeued item {item}')
            return item
        except Exception as e:
            self.logger.error(f'Error dequeuing item: {e}')

    def is_empty(self):
        return len(self.items) == 0
