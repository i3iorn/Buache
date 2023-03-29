import v3 as app
import unittest
from v3.address.parser import AddressParser

ap = AddressParser()
addresses = [
    "1600 Pennsylvania Ave NW, Washington, DC 20500, United States",
    "10 Downing Street, Westminster, London SW1A 2AA, United Kingdom",
    "Champs-Élysées, Paris, France",
    "Brandenburg Gate, Pariser Platz, Berlin, Germany",
    "1 Macquarie St, Sydney NSW 2000, Australia",
    "Calle de Serrano, Madrid, Spain",
    "Roppongi Hills Mori Tower, 6 Chome-10-1 Roppongi, Minato City, Tokyo 106-0032, Japan",
    "Rua da Gloria, Rio de Janeiro - RJ, 20241-180, Brazil",
    "Hans Christian Andersens Blvd. 18, 1553 København V, Denmark",
    "Rua Augusta, Lisbon, Portugal",
    "Danagränd 7, 17566 Järfälla",
    "Oxenstiernas allé 23 17464 Sundbyberg",
    "Oxbacksgatan 3 lgh 1213 72461	Västerås"
]

for address in addresses:
    print(address)
    ap_list = ap.parse_address(address)

unittest.main()
