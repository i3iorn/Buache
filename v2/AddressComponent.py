class AddressComponent:
    ADDRESS_COMPONENT_TYPES = [
        "apartment_number",
        "floor",
        "entrance",
        "building",
        "street_number",
        "street_name",
        "street_suffix",
        "block",
        "postal_code",
        "administrative_region_small",
        "city",
        "administrative_region_medium",
        "municipality",
        "administrative_region_large",
        "country",
        "continent"
    ]
    def __name__(self):
        return NotImplementedError
