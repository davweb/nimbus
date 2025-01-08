"""Device module for Console testing"""

import sys
from select import select


def init():
    """Initialise the device - not needed for console"""


def display(bus_stop_name, buses, last_updated, _):
    """Send bus information to standard output"""

    print(bus_stop_name)

    for (bus, destination, due) in buses:
        print(bus, destination, due)

    print(last_updated)


def wait_for_press(timeout_seconds):
    """Wait for an enter key press or timeout"""

    rlist, _, _ = select([sys.stdin], [], [], timeout_seconds)

    if rlist:
        sys.stdin.readline()
        return True

    return False
