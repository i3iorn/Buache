import json
import os
from pathlib import Path

with open(Path('Config/adapters.json').absolute(), 'r') as adapters:
    ADAPTERS = json.load(adapters)

with open(Path('../.env').absolute(), 'r', encoding='utf8') as env:
    for line in env:
        key, value = line.split('=')
        os.environ[key] = value

CACHE_LIMIT = os.getenv('CACHE_LIMIT') or 3600
LOG_LEVEL = os.getenv('LOG_LEVEL') or 'WARNING'
