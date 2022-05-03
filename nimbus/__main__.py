"""Display bus times on an e-ink screen"""

import math
import argparse
from nimbus import nextbus


def print_buses(bus_stop_name, buses, last_updated):
    """Send bus information to standard output"""

    print(bus_stop_name)

    for (bus, destination, due) in buses:
        print(bus,destination,due)

    print(last_updated)


def main():
    """Entrypoint function"""

    parser = argparse.ArgumentParser(description='Display bus times on an e-ink screen.')
    parser.add_argument('-c', '--console', action='store_true',
        help='Display output on the console')
    args = parser.parse_args()
    console = args.console

    # Conditional import so we can test code on non-RPi systems
    if not console:
        from nimbus import epaper

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
            due = f'{minutes} mins'

        buses.append((bus, destination, due))

    last_updated = refresh_time.strftime('Last updated %H:%M')

    if console:
        print_buses(bus_stop_name, buses, last_updated)
    else:
        epaper.display(bus_stop_name, buses, last_updated)

if __name__ == '__main__':
    main()
