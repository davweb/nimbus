"""Display bus times on an e-ink screen"""

from datetime import datetime
from pathlib import Path
import math
import argparse
from nimbus import oxontime
from nimbus import bustimesorg

def print_buses(bus_stop_name, buses, last_updated):
    """Send bus information to standard output"""

    print(bus_stop_name)

    for (bus, destination, due) in buses:
        print(bus, destination, due)

    print(last_updated)


def format_due(due_time, refresh_time):
    """Format bus due time"""

    seconds = (due_time - refresh_time).total_seconds()

    if seconds == 0:
        return 'due'

    if seconds < 61:
        return '1 min'

    minutes = math.ceil(seconds / 60)

    if minutes <= 60:
        return f'{minutes} mins'

    return due_time.strftime('%-H:%M')


def parse_args():
    """Parse the command line arguments"""

    parser = argparse.ArgumentParser(description='Display bus times on an e-ink screen.')
    parser.add_argument('-c', '--console', action='store_true',
                        help='Display output on the console')
    parser.add_argument('-f', '--heartbeat_file', action='store',
                        help='File to touch on every update')
    parser.add_argument('-o', '--oxontime', action='store_true',
                        help='Use oxontime.com instead of bustimes.org for bus times')
    parser.add_argument('bus_stop_id', nargs='+', help='Bus Stop ID')

    args = parser.parse_args()
    return args.console, args.heartbeat_file, args.oxontime, args.bus_stop_id


def fetch_bus_times(bus_stop_id, use_oxontime):
    """Fetch the bus times"""

    try:
        if use_oxontime:
            (bus_stop_name, refresh_time, raw_buses) = oxontime.extract_bus_information(bus_stop_id)
        else:
            (bus_stop_name, refresh_time, raw_buses) = bustimesorg.extract_bus_information(bus_stop_id)

        buses = []

        for (bus, destination, due_time) in raw_buses[:3]:
            due = format_due(due_time, refresh_time)
            buses.append((bus, destination, due))

    except BaseException:
        bus_stop_name = 'Error fetching times'
        buses = []
        refresh_time = datetime.now()

    return bus_stop_name, buses, refresh_time


def main():
    """Entrypoint function"""

    console, heartbeat_file, use_oxontime, bus_stops = parse_args()

    # Conditional import so we can test code on non-RPi systems
    if not console:
        from nimbus import epaper
        from nimbus import touch
        touch.init()

    change = True
    bus_stop_index = -1

    while True:
        if change:
            bus_stop_index += 1
            bus_stop_index %= len(bus_stops)
            bus_stop_id = bus_stops[bus_stop_index]

        (bus_stop_name, buses, refresh_time) = fetch_bus_times(bus_stop_id, use_oxontime)
        last_updated = refresh_time.strftime('Last updated %H:%M')

        if heartbeat_file:
            Path(heartbeat_file).touch()

        if console:
            print_buses(bus_stop_name, buses, last_updated)
            break

        epaper.display(bus_stop_name, buses, last_updated, change)
        change = touch.wait_for_touch(60)


if __name__ == '__main__':
    main()
