import logging

from src.address import Address


class Application:
    MODES = [
        'PRODUCTION',
        'QUALITY_ASSURANCE',
        'DEVELOPMENT'
    ]

    def __init__(
            self,
            mode: MODES = 'DEVELOPMENT'
    ):
        self.full = None
        self.log = logging.getLogger(__name__)
        if mode == 'PRODUCTION':
            logging.getLogger().setLevel('INFO')
        elif mode == 'QUALITY_ASSURANCE':
            logging.getLogger().setLevel('DEBUG')
        else:
            logging.getLogger().setLevel('TRACE')

        self.log.info(f'Running app with logg level: {self.log.getEffectiveLevel()}')

    def check_address(self, string):
        return Address(string)
