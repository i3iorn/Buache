class Rule:
    def __init__(self, name, condition, error_message):
        self.name = name
        self.condition = getattr(self, condition)
        self.error_message = error_message

    def validate(self, value):
        if not self.condition(value):
            raise ValueError(self.error_message)

    @staticmethod
    def is_non_empty_string(value):
        return isinstance(value, str) and len(value) > 0

    @staticmethod
    def is_positive_integer(value):
        return isinstance(value, int) and value > 0
