import logging


class BuacheFormatter(logging.Formatter):
    level1 = "\x1b[38;5;243m"
    level2 = "\x1b[38;5;248m"
    level3 = "\x1b[38;5;253m"
    level4 = "\x1b[38;5;15m"
    level5 = "\x1b[38;5;43m"
    level6 = "\x1b[38;5;3m"
    level7 = "\x1b[38;5;166m"
    level8 = "\x1b[38;5;160m"
    reset = "\x1b[0m"
    format = "[%(asctime)s] [%(name)30s] [%(funcName)30s] [%(levelname)8s] [%(lineno)4d] \n" \
             "======================================================================================================" \
             "\n%(message)s\n "

    FORMATS = {
        logging.TRACE: level1 + format + reset,
        logging.DEBUG2: level2 + format + reset,
        logging.DEBUG: level3 + format + reset,
        logging.VERBOSE: level4 + format + reset,
        logging.INFO: level5 + format + reset,
        logging.WARNING: level6 + format + reset,
        logging.ERROR: level7 + format + reset,
        logging.CRITICAL: level8 + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
