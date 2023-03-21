from src.Adapters import BaseAdapter
from src.address import Address


class Api(BaseAdapter):
    def __init__(self, config):
        super().__init__(config)

    def status(self) -> bool:
        pass

    def validate_address(self, address: Address) -> bool:
        pass

    def get_new_data(self, address: Address) -> bool:
        pass
