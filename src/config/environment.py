import json
import os
from pathlib import Path

with open(Path('src/config/adapters.json').absolute(), 'r') as adapters:
    ADAPTERS = json.load(adapters)

with open(Path('.env').absolute(), 'r', encoding='utf8') as env:
    for line in env:
        key, value = line.split('=')
        os.environ[key] = value

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent

QUEUE_MAX_SIZE = os.getenv('QUEUE_MAX_SIZE') or 100

CACHE_TTL = os.getenv('CACHE_TTL') or 28800

MONITOR_SLEEP = os.getenv('MONITOR_SLEEP') or 2

LOG_LEVEL = os.getenv('LOG_LEVEL') or 'WARNING'
LOG_PATH = os.getenv('LOG_PATH') or 'data/Logs'

