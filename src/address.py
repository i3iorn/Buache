class Address:
    def __init__(self, **kwargs):
        self.street_name = kwargs['street_name'] or None
        self.street_number = kwargs['street_number'] or None
        self.street_number_range = kwargs['street_number_range'] or None
        self.entrance = kwargs['entrance'] or None
        self.zip = kwargs['zip'] or None
        self.city = kwargs['city'] or None
        self.municipality = kwargs['municipality'] or None
        self.region = kwargs['region'] or None
        self.apartment_number = kwargs['apartment_number'] or None
        self.coordinates = kwargs['coordinates'] or None
        self.county = kwargs['county'] or None
        self.country = kwargs['country'] or None

    @property
    def street_name(self) -> str:
        return self._street_name

    @street_name.setter
    def street_name(self, value: str) -> None:
        self._street_name = value

    @property
    def street_number(self) -> str:
        return self._street_number

    @street_number.setter
    def street_number(self, value: str) -> None:
        self._street_number = value

    @property
    def entrance(self) -> str:
        return self._entrance

    @entrance.setter
    def entrance(self, value: str) -> None:
        self._entrance = value

    @property
    def zip(self) -> str:
        return self._zip

    @zip.setter
    def zip(self, value: str) -> None:
        self._zip = value

    @property
    def city(self) -> str:
        return self._city

    @city.setter
    def city(self, value: str) -> None:
        self._city = value

    @property
    def municipality(self) -> str:
        return self._municipality

    @municipality.setter
    def municipality(self, value: str) -> None:
        self._municipality = value

    @property
    def region(self) -> str:
        return self._region

    @region.setter
    def region(self, value: str) -> None:
        self._region = value

    @property
    def apartment_number(self) -> str:
        return self._apartment_number

    @apartment_number.setter
    def apartment_number(self, value: str) -> None:
        self._apartment_number = value
