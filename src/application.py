import logging
import importlib
import tracemalloc
from time import time, sleep

from src import AdapterCountException, BuacheException, Monitor
from src.config.environment import ADAPTERS, MONITOR_SLEEP
from src.queue import Queue


class Buache:
    def __init__(self):
        self.logger = logging.getLogger('Application')
        self.logger.propagate = False
        self.active_adapters = []
        self.errors = []
        self.queue = Queue()

    def start(self) -> None:
        """
        Start the application.
        """
        tracemalloc.start()
        self.logger.info(f"Logging level is set to {self.logger.getEffectiveLevel()}")
        try:
            self._load_adapters()
            self._main_loop()
        except BuacheException as e:
            self.logger.critical('Fatal error in application. {}'.format(e))
            raise BuacheException(
                'Fatal application error occurred. Unable to continue. See logs for further details.'
            ) from e
        except KeyboardInterrupt:
            self.logger.info('Process interrupted by user.')
        finally:
            tracemalloc.stop()

    def _main_loop(self) -> None:
        """
        The main loop of the application.
        """
        start = time()
        last = start
        try:
            while True:
                self._run_input_monitor()

                if not self.queue.empty():
                    self._get_next_item()

                self._handle_errors()
                self._log_status(start, last)
                self._log_resources_used()

                sleep(MONITOR_SLEEP)
                last = time()
        except AdapterCountException:
            self.logger.error('No active adapters.')
        except Exception as e:
            self.logger.error(f'Error occurred in main loop. {e}')

    def _load_adapters(self) -> None:
        """
        Load any configured input adapters.
        """
        for adptr in ADAPTERS:
            if adptr['name'] not in [a.name for a in self.active_adapters]:
                self.logger.debug(f"Processing adapter {adptr['name']}")
                new_adapter = importlib.import_module('src.adapters.{}'.format(adptr['type']))
                class_ = getattr(new_adapter, str(adptr['type']).capitalize())
                self.active_adapters.append(class_(adptr))
        if len(self.active_adapters) == 0:
            self.logger.debug('There are no active adapters')
        elif len(self.active_adapters) == 1:
            self.logger.debug('There is 1 active adapter')
        elif len(self.active_adapters) > 1:
            self.logger.debug(f'There are {len(self.active_adapters)} active adapters')

    def _run_input_monitor(self):
        """
        Run input monitor.
        """
        pre_load_adapters = [adapter for adapter in self.active_adapters if adapter.pre_load]
        if len(pre_load_adapters) > 0:
            self.logger.debug('Starting monitoring for adapters that needs to be pre loaded. ')
            monitor = Monitor(self.active_adapters)

    def _get_next_item(self):
        return self.queue.dequeue()

    def _handle_errors(self):
        """
        If there are any non-critical errors it's time to handle them.
        """
        for error in self.errors:
            log_level_msg_ = getattr(logging, error.level)
            log_level_msg_(error.msg)

    def _log_status(self, start, last):
        """
        Add some trace logs to keep track of the main loop status.
        """
        diff = time() - start
        last_diff = time() - last
        self.logger.trace(f'Application has been alive for {diff} seconds.')
        self.logger.trace(f'Last main loop iteration took {last_diff} seconds.')

    def _log_resources_used(self):
        """
        Log resources used
        """
        if tracemalloc.get_traced_memory()[0] > 6000000 \
                or tracemalloc.get_traced_memory()[0] > 10000000:
            self.logger.warning(tracemalloc.get_traced_memory())

