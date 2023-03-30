import logging

from src.app import Application

"""
Remember to add all new classes to __all__
"""

__all__ = [
    'Application',
    'run'
]
logger = logging.getLogger(__name__)
logger.debug(f'Configuration is loaded.')


def run(**kwargs) -> Application:
    return Application(**kwargs)
