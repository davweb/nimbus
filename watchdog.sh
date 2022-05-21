#!/bin/bash

HEARTBEAT_FILE=/tmp/heartbeat
AGE_MINUTES=3
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if test -z $(find ${HEARTBEAT_FILE} -mmin -${AGE_MINUTES})
then
    echo $(date -Iminutes) Watchdog rebooting system >>${SCRIPT_DIR}/watchdog.log
    sudo reboot
fi
