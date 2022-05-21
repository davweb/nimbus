"""Code for working with the touch screen"""

import time
import threading
# Import so GPIO is initialised
from nimbus import epaper

from TP_lib import gt1151

TOUCH = gt1151.GT1151()
TOUCH.GT_Reset()
GT_Dev = gt1151.GT_Development()
GT_Old = gt1151.GT_Development()

SLEEP_TIME = 0.01

def _touch_thread():
    """Poll for touches"""

    while True:
        if TOUCH.digital_read(TOUCH.INT) == 0:
            GT_Dev.Touch = 1
        else:
            GT_Dev.Touch = 0

        # Quick sleep to stop this using all the CPU
        time.sleep(SLEEP_TIME)

def init():
    """Initialise touch background thread"""
    thread = threading.Thread(target = _touch_thread)
    thread.daemon = True
    thread.start()


def wait_for_touch(timeout_seconds):
    """Wait for a touch or for time to pass"""

    end_time = time.time() + timeout_seconds

    while time.time() < end_time:
        # Quick sleep to stop this using all the CPU
        time.sleep(SLEEP_TIME)

        TOUCH.GT_Scan(GT_Dev, GT_Old)

        if GT_Old.X[0] != GT_Dev.X[0] or GT_Old.Y[0] != GT_Dev.Y[0] or GT_Old.S[0] != GT_Dev.S[0]:
            return True

    return False
