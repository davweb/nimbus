"""Get next bus time by parsing a web page"""

from datetime import timedelta
import re
from bs4 import BeautifulSoup
from dateutil import parser
import requests


TIMES_URL = 'http://www.nextbuses.mobi/WebView/BusStopSearch/BusStopSearchResults/{}'
PATTERN_AT = re.compile(r'(.*) at (\d+:\d+)$')
PATTERN_IN = re.compile(r'(.*) in (\d+) mins?')


def _extract_refresh_time(root):
    """Extract the refresh time from a bus stop page"""

    refresh_time_span = root.select('div.content h5 span')[1]
    return parser.parse(refresh_time_span.text)


def _extract_bus_arrivals(root):
    """Extract the upcoming bus times from a bus stop page"""

    refresh_time = _extract_refresh_time(root)
    buses = []

    for upcoming_bus in root.select('tr'):
        bus_number_element = upcoming_bus.select('td.Number p.Stops a')
        bus_details_element = upcoming_bus.select('td:not(.Number) p.Stops')

        if not bus_number_element or not bus_details_element:
            continue

        bus_number = bus_number_element[0].text
        bus_details = bus_details_element[0].text

        in_result = PATTERN_IN.match(bus_details)
        at_result = PATTERN_AT.match(bus_details)

        if in_result:
            destination = in_result[1]
            minutes = int(in_result[2])
            bus_time = refresh_time + timedelta(minutes=minutes)
        elif at_result:
            destination = at_result[1]
            bus_time = parser.parse(at_result[2])
        else:
            continue

        comma_index = destination.find(',')

        if comma_index != -1:
            destination = destination[:comma_index]

        buses.append((bus_number, destination, bus_time))

    return buses


def extract_bus_information(bus_stop_id):
    """Download bus time information page and return the data"""

    url = TIMES_URL.format(bus_stop_id)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    refresh_time = _extract_refresh_time(soup)
    buses = _extract_bus_arrivals(soup)

    return (refresh_time, buses)
