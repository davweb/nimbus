"""Get next bus time by parsing a web page"""

from datetime import timedelta
import re
from bs4 import BeautifulSoup
from dateutil import parser
import requests


TIMES_URL = 'http://www.nextbuses.mobi/WebView/BusStopSearch/BusStopSearchResults/{}'
PATTERN_DUE = re.compile(r'(.*) DUE$')
PATTERN_DAY = re.compile(r'(.*) at (\d+:\d+) \((\w+)\)$')
PATTERN_AT = re.compile(r'(.*) at (\d+:\d+)$')
PATTERN_IN = re.compile(r'(.*) in (\d+) mins?')
PATTERN_STOP = re.compile(r'Departures for (((\w+)\s+)*\w+)')

PARSER_CONFIG = parser.parserinfo(dayfirst=True)


def _extract_refresh_time(root):
    """Extract the refresh time from a bus stop page"""

    refresh_time_span = root.select('div.content h5 span')[1]
    return parser.parse(refresh_time_span.text, PARSER_CONFIG)


def _extract_stop_name(root):
    """Get the bus stop name"""
    stop_name_element = root.select('div.content h2')[0]
    stop_name = stop_name_element.text

    if result := PATTERN_STOP.match(stop_name):
        stop_name = result[1]

    return stop_name


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

        if due_result := PATTERN_DUE.match(bus_details):
            destination = due_result[1]
            bus_time = refresh_time
        elif in_result := PATTERN_IN.match(bus_details):
            destination = in_result[1]
            minutes = int(in_result[2])
            bus_time = refresh_time + timedelta(minutes=minutes)
        elif at_result := PATTERN_AT.match(bus_details):
            destination = at_result[1]
            bus_time = parser.parse(at_result[2], PARSER_CONFIG)
        elif at_result := PATTERN_DAY.match(bus_details):
            destination = at_result[1]
            bus_time = parser.parse(at_result[2], PARSER_CONFIG)

            #  Assume buses for later days are only ever for tomorrow
            bus_time += timedelta(days=1)
        else:
            continue

        destination = destination.replace('and', '&')
        comma_index = destination.find(',')

        if comma_index != -1:
            destination = destination[:comma_index]

        buses.append((bus_number, destination, bus_time))

    return buses


def extract_bus_information(bus_stop_id):
    """Download bus time information page and return the data"""

    url = TIMES_URL.format(bus_stop_id)
    page = requests.get(url, timeout=60)
    soup = BeautifulSoup(page.content, 'html.parser')

    stop_name = _extract_stop_name(soup)
    refresh_time = _extract_refresh_time(soup)
    buses = _extract_bus_arrivals(soup)

    return (stop_name, refresh_time, buses)
