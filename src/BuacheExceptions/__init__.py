class Error:
    def __init__(self, msg: str, level: int = 20):
        self.msg = msg
        self.level = level


class BuacheException(Exception):
    pass
