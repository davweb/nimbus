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


def format_due(due_time, refresh_time):
    seconds = (due_time - refresh_time).total_seconds()

    if seconds == 0:
        return 'due'

    if seconds < 61:
        return  '1 min'

    minutes = math.ceil(seconds / 60)

    if minutes <= 60:
        return f'{minutes} mins'

    return due_time.strftime('%-H:%M')


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
        from nimbus import touch
        touch.init()

    change = True
    bus_stop_id = None

    while True:
        if change:
            if bus_stop_id == 'oxfadgdw':
                bus_stop_id = 'oxfadgpm'
                bus_stop_name = 'Raleigh Park Road'
            else:
                bus_stop_id = 'oxfadgdw'
                bus_stop_name = 'Laburnum Road'

        (refresh_time, raw_buses) = nextbus.extract_bus_information(bus_stop_id)

        buses = []

        for (bus, destination, due_time) in raw_buses[:3]:
            due = format_due(due_time, refresh_time)
            buses.append((bus, destination, due))

        last_updated = refresh_time.strftime('Last updated %H:%M')

        if console:
            print_buses(bus_stop_name, buses, last_updated)
            break

        epaper.display(bus_stop_name, buses, last_updated, change)
        change = touch.wait_for_touch(60)


if __name__ == '__main__':
    main()
