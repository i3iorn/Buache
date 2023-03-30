from enum import Enum, auto


class AddressComponentType(Enum):
    STREET_NAME = auto()
    STREET_NUMBER = auto()
    BUILDING = auto()
    ENTRANCE = auto()
    APARTMENT = auto()
    CO = auto()
    BLOCK = auto()
    POSTAL_CODE = auto()
    CITY = auto()
    STATE = auto()
    COUNTRY = auto()


class AddressComponent:
    def __init__(self, component_type: AddressComponentType, component_value: str, confidence: float, position: int):
        self.position = position
        self.component_type = component_type
        self.component_value = component_value
        self.confidence = confidence

    @property
    def component_type(self) -> AddressComponentType:
        return self._component_type

    @component_type.setter
    def component_type(self, value: AddressComponentType) -> None:
        self._component_type = value

    @property
    def confidence(self) -> float:
        return self._confidence

    @confidence.setter
    def confidence(self, value: float) -> None:
        self._confidence = value

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value

    @property
    def component_value(self) -> str:
        return self._component_value

    @component_value.setter
    def component_value(self, value: str) -> None:
        self._component_value = value

    def __lt__(self, other_component: 'AddressComponent') -> bool:
        return self.confidence < other_component.confidence

    def sort_by_component_order(self, items, country):
        return sorted(items, key=key_func)
