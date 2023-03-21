
import logging
import src.Config.app
from time import sleep, time

from BuacheExceptions import BuacheException


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

    """
    Load any configured input adapters.
    """
    adapters = []


    try:
        while True:
            """
            Run input monitor.
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
