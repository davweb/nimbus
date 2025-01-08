"""Device module for the Raspberry Pi Waveshare e-ink display"""

from . import epaper
from . import touch


def init():
    """Initialise the device"""

    touch.init()


def display(bus_stop_name, buses, last_updated, force_full_update):
    """Display bus information on the e-ink screen"""

    epaper.display(bus_stop_name, buses, last_updated, force_full_update)


def wait_for_press(timeout_seconds):
    """Wait for a screen press or timeout"""

    return touch.wait_for_touch(timeout_seconds)
