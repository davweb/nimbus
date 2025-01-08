"""Get next bus time by parsing a web page"""

import datetime
from bs4 import BeautifulSoup
from dateutil import parser
import requests
from .config import CONFIG

TIMES_URL = 'https://bustimes.org/stops/{}'
PARSER_CONFIG = parser.parserinfo(dayfirst=True)


def _extract_stop_name(root):
    """Get the bus stop name"""
    stop_name_element = root.find('h1')
    stop_name = stop_name_element.text.strip()
    return stop_name


def _extract_bus_arrivals(root):
    """Extract the upcoming bus times from a bus stop page"""

    buses = []

    for upcoming_bus in root.select('tr'):
        upcoming_bus_td = upcoming_bus.select('td')

        if len(upcoming_bus_td) < 3:
            continue

        bus_number = upcoming_bus_td[0].text.strip()
        destination = upcoming_bus_td[1].text.strip()

        registration = upcoming_bus_td[1].find('div', class_='vehicle')

        if registration:
            destination = destination.replace(registration.text, '').strip()

        if len(upcoming_bus_td) > 3:
            bus_time_text = upcoming_bus_td[3].text.strip() or upcoming_bus_td[2].text.strip()
        else:
            bus_time_text = upcoming_bus_td[2].text.strip()

        if not bus_number or not destination or not bus_time_text:
            continue

        bus_time = parser.parse(bus_time_text, PARSER_CONFIG)

        buses.append((bus_number, destination, bus_time))

    return buses


def extract_bus_information(bus_stop_id):
    """Download bus time information page and return the data"""

    url = TIMES_URL.format(bus_stop_id)
    page = requests.get(url, timeout=CONFIG.request_timeout)
    soup = BeautifulSoup(page.content, 'html.parser')

    stop_name = _extract_stop_name(soup)
    buses = _extract_bus_arrivals(soup)

    #  bustimes.org has no refresh time on the page so we set it to the start of the current minute
    refresh_time = datetime.datetime.now().replace(second=0, microsecond=0)

    return (stop_name, refresh_time, buses)
