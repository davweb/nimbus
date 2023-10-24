"""Tests for parsing bus times"""

# Unit tests are allowed to access protected methods
# pylint: disable=protected-access

import datetime
import unittest
from bs4 import BeautifulSoup
from nimbus import nextbus


def parse_fixture(fixture_file):
    """Fetch HTML from a fixture file and parse it"""

    with open(f'test/fixtures/{fixture_file}', encoding='UTF-8') as fixture:
        contents = fixture.read()
        return BeautifulSoup(contents, 'html.parser')


class TestParsing(unittest.TestCase):
    """Tests for parsing bus times"""

    def setUp(self):
        self.soon = parse_fixture('soon.html')
        self.due = parse_fixture('due.html')
        self.later = parse_fixture('later.html')
        self.next_day = parse_fixture('next-day.html')
        self.mixed = parse_fixture('mixed.html')

    def test_extract_stop_name(self):
        """Test extracting stop name"""

        result = nextbus._extract_stop_name(self.soon)
        self.assertEqual(result, 'Raleigh Park Road')

    def test_extract_refresh_time(self):
        """Test extracting refresh time"""

        result = nextbus._extract_refresh_time(self.soon)
        self.assertEqual(result, datetime.datetime(2022, 5, 16, 7, 55))

    def test_extract_bus_arrivals_bus(self):
        """Test extracting upcoming bus name"""

        results = nextbus._extract_bus_arrivals(self.soon)
        bus = results[0][0]
        self.assertEqual(bus, 'U1')

    def test_extract_bus_arrivals_destination(self):
        """Test extracting upcoming bus destination"""

        results = nextbus._extract_bus_arrivals(self.soon)
        destination = results[0][1]
        self.assertEqual(destination, 'Wheatley')

    def test_extract_bus_arrivals_soon(self):
        """Test extracting upcoming bus time when it's shown in minutes"""

        results = nextbus._extract_bus_arrivals(self.soon)
        time = results[0][2]
        self.assertEqual(time, datetime.datetime(2022, 5, 16, 8, 5))

    def test_extract_bus_arrivals_due(self):
        """Test extracting upcoming bus time when it's shown as due"""

        refresh_time = nextbus._extract_refresh_time(self.due)
        results = nextbus._extract_bus_arrivals(self.due)
        time = results[0][2]
        self.assertEqual(time, refresh_time)

    def test_extract_bus_arrivals_later(self):
        """Test extracting upcoming bus time when it's shown as a time"""

        results = nextbus._extract_bus_arrivals(self.later)
        time = results[1][2]
        self.assertEqual(time.time(), datetime.time(7, 36))
        self.assertEqual(time.date(), datetime.date.today())

    def test_extract_bus_arrivals_next_day(self):
        """Test extracting upcoming bus time when it's shown as the next day"""

        results = nextbus._extract_bus_arrivals(self.next_day)
        time = results[0][2]
        self.assertEqual(time.time(), datetime.time(6, 36))
        self.assertEqual(time.date(), datetime.date.today() + datetime.timedelta(days=1))

    def test_extract_bus_arrivals(self):
        """Test extracting multiple bus times is done correctly"""

        results = nextbus._extract_bus_arrivals(self.mixed)

        self.assertEqual(len(results), 4)


if __name__ == '__main__':
    unittest.main()
