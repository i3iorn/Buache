import importlib
import logging
import src.Config.app
from time import sleep, time

from BuacheExceptions import BuacheException, AdapterCountException
from src.Config.environment import ADAPTERS
from src.Monitor import Monitor


def start_application():
    """
    The main loop of the application.

    :return:
    """

    """
    Set some initial states.
    """
    start = time()
    last = start
    logger = logging.getLogger()
    logger.info('Logging level is set to {}'.format(logger.getEffectiveLevel()))
    errors = []
    active_adapters = []

    try:
        while True:
            """
            Load any configured input adapters.
            """
            for adptr in ADAPTERS:
                if adptr['name'] not in [a.name for a in active_adapters]:
                    logger.debug('Processing adapter {}'.format(adptr['name']))
                    """ Get the adapter module based on configured type."""
                    new_adapter = importlib.import_module('src.Adapters.{}'.format(adptr['type']))

                    """ Get the adapter class. """
                    class_ = getattr(new_adapter, str(adptr['type']).capitalize())

                    """ Add new adapter to active adapters. """
                    active_adapters.append(class_(adptr))

            if len(active_adapters) == 0:
                logger.debug('There are no active adapters')
            elif len(active_adapters) == 1:
                logger.debug('There is 1 active adapter')
            elif len(active_adapters) > 1:
                logger.debug('There are {} active adapters'.format(len(active_adapters)))
            else:
                raise AdapterCountException

            """
            Run input monitor.
            """
            pre_load_adapters = [adapter for adapter in active_adapters if adapter.pre_load]
            if len(pre_load_adapters) > 0:
                logger.debug('Starting monitoring for adapters that needs to be pre loaded. ')
                monitor = Monitor(active_adapters)

            """
            Get next item in queue.
            """


            """
            If there are any non critical errors its time to handle them.
            """
            for error in errors:
                log_level_msg_ = getattr(logging, error.level)
                log_level_msg_(error.msg)

            """
            Add some trace logs to keep track of the main loop status.
            """
            diff = time() - start
            last_diff = time() - last
            logger.trace('Application has been alive for {} seconds.'.format(diff))
            logger.trace('Last main loop iteration took {} seconds.'.format(last_diff))
            last = time()

            """
            Sleep for one second add some breathing room.
            """
            sleep(1)
    except BuacheException as e:
        logger.critical('Fatal error in application. {}'.format(e))
        raise BuacheException('Fatal application error occured. Unable to continue. See logs for further details.') from e


start_application()
