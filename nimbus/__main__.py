"""Display bus times on an e-ink screen"""

from datetime import datetime
from pathlib import Path
import math
from .config import CONFIG

if CONFIG.console:
    from . import console as device
else:
    from . import device

match CONFIG.source:
    case 'oxontime':
        from . import oxontime as bustimes
    case 'nextbuses':
        from . import nextbuses as bustimes
    case 'bustimes':
        from . import bustimes
    case unknown:
        raise ValueError(f'Unknown source for bus times: {unknown}')


def format_due(due_time, refresh_time):
    """Format bus due time"""

    seconds = (due_time - refresh_time).total_seconds()

    if seconds <= 0:
        return 'due'

    if seconds < 61:
        return '1 min'

    minutes = math.ceil(seconds / 60)

    if minutes <= 60:
        return f'{minutes} mins'

    return due_time.strftime('%-H:%M')


def fetch_bus_times(bus_stop_id):
    """Fetch the bus times"""

    try:
        (bus_stop_name, refresh_time, raw_buses) = bustimes.extract_bus_information(bus_stop_id)
        buses = []

        for (bus, destination, due_time) in raw_buses[:3]:
            due = format_due(due_time, refresh_time)
            buses.append((bus, destination, due))

    except BaseException:  # pylint: disable=broad-exception-caught
        bus_stop_name = 'Error fetching times'
        buses = []
        refresh_time = datetime.now()

    return bus_stop_name, buses, refresh_time


def main():
    """Entrypoint function"""

    device.init()

    change = False
    bus_stop_index = 0
    bus_stop_id = CONFIG.bus_stops[bus_stop_index]

    while True:
        (bus_stop_name, buses, refresh_time) = fetch_bus_times(bus_stop_id)
        last_updated = refresh_time.strftime('Last updated %H:%M')

        if CONFIG.heartbeat_file:
            Path(CONFIG.heartbeat_file).touch()

        device.display(bus_stop_name, buses, last_updated, change)
        change = device.wait_for_press(60)

        if change:
            bus_stop_index += 1
            bus_stop_index %= len(CONFIG.bus_stops)
            bus_stop_id = CONFIG.bus_stops[bus_stop_index]


if __name__ == '__main__':
    main()
