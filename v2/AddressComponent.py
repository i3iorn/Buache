import logging
from config import ADDRESS_COMPONENT_TYPES


class AddressComponent:
    def __init__(self, ad_type: ADDRESS_COMPONENT_TYPES):
        self.log = logging.getLogger(__name__)
        self.component_type = ad_type
