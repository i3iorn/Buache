from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.address import Address


class BaseAdapter:
    def __init__(self):
        pass

    def get_new_data(self, address: Address) -> bool:
        raise NotImplementedError

    def status(self) -> bool:
        raise NotImplementedError

    def validate_address(self, address: Address) -> bool:
        raise NotImplementedError
