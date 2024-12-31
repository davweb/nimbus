#!/usr/bin/bash

touch /tmp/heartbeat
cd /home/pi/nimbus
source .venv/bin/activate
python -m nimbus -f /tmp/heartbeat 340000006R1 340000006R2 >nimbus.out 2>&1
