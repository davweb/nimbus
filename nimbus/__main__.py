"""Display bus times on an e-ink screen"""

from nimbus import nextbus
from nimbus import epaper
from datetime import datetime
import math

def main():
    """Entrypoint function"""

    #bus_stop_id = 'oxfadgdw'
    bus_stop_id = 'oxfadgpm'
    bus_stop_name = 'Raleigh Park Road'

    (refresh_time, raw_buses) = nextbus.extract_bus_information(bus_stop_id)

    buses = []

    for (bus, destination, due) in raw_buses[:3]:
        seconds = (due - refresh_time).total_seconds()

        if seconds == 0:
            due = 'due'
        elif seconds < 61:
            due = '1 min'
        else:
            minutes = math.ceil(seconds / 60)
            due = '{} mins'.format(minutes)

        buses.append((bus, destination, due))

    epaper.display(bus_stop_name, buses, refresh_time.strftime('Last updated %H:%M'))

if __name__ == '__main__':
    main()
