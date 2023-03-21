import json
import logging
import os
from pathlib import Path

with open(Path('config/adapters.json').absolute(), 'r') as adapters:
    ADAPTERS = json.load(adapters)

with open(Path('../.env').absolute(), 'r', encoding='utf8') as env:
    for line in env:
        key, value = line.split('=')
        os.environ[key] = value

CACHE_LIMIT = os.getenv('CACHE_LIMIT') or 3600

MONITOR_SLEEP = os.getenv('MONITOR_SLEEP') or 2

LOG_LEVEL = os.getenv('LOG_LEVEL') or 'WARNING'
LOG_PATH = os.getenv('LOG_PATH') or 'data/Logs'

