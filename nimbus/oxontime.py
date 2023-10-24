import requests
import json
from dateutil import parser

LOCATIONS_URL = 'https://oxontime.com/pwi/getShareLocations'
TIMES_URL = 'https://oxontime.com/pwi/departureBoard/{}'
STOPS = None

def _bus_stop_name(bus_stop_id):
    global STOPS

    if STOPS is None:
        STOPS = {}
        page = requests.get(LOCATIONS_URL)
        locations = json.loads(page.content)

        for location in locations:
            STOPS[location['location_code']] = location['location_name']

    return STOPS[bus_stop_id]


def _bus_details(bus):
    route = bus['route_code']
    destination = bus['destination']

    departure_time = bus['expected_arrival_time']

    if not departure_time:
        departure_time = bus['aimed_arrival_time']

    departure_time = parser.parse(departure_time)

    return (route, destination, departure_time)


def extract_bus_information(bus_stop_id):
    """Download bus time information page and return the data"""

    url = TIMES_URL.format(bus_stop_id)
    page = requests.get(url)
    data = json.loads(page.content)[bus_stop_id]

    stop_name = _bus_stop_name(bus_stop_id)
    refresh_time = parser.parse(data['time'])
    buses = [_bus_details(bus) for bus in data['calls']]

    return (stop_name, refresh_time, buses)