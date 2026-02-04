#!/usr/bin/bash

# Install dialog
sudo apt-get install -qq dialog

export DIALOGOPTS="--backtitle \"Nimbus Set Up\" --clear"
exec 3>&1

SOURCE=$(dialog --menu "Select the source of Bus Time data" 10 39 3 \
    1 www.nextbuses.mobi \
    2 bustimes.org \
    3 oxontime.com \
    2>&1 1>&3)

if [ $? -ne 0 ]
then
    exit 1
fi

BUS_STOPS=$(dialog --form "Enter your Bus Stop IDs" 12 30 0 \
    "1:" 1 1 "" 1 4 20 20 \
    "2:" 2 1 "" 2 4 20 20 \
    "3:" 3 1 "" 3 4 20 20 \
    "4:" 4 1 "" 4 4 20 20 \
    "5:" 5 1 "" 5 4 20 20 \
    2>&1 1>&3)

if [ $? -ne 0 ]
then
    exit 1
fi

DISPLAY_VERSION=$(dialog --menu "Select your version of the Waveshare Display" 11 39 3 \
    2 "Version 2" \
    3 "Version 3" \
    4 "Version 4" \
    2>&1 1>&3)

if [ $? -ne 0 ]
then
    exit 1
fi

clear

# Enable SPI
sudo raspi-config nonint do_spi 0

# Enable I2C
sudo raspi-config nonint do_i2c 0

# Install other required packages
sudo apt-get install -q -y gcc git liblgpio-dev libjpeg-dev python3-dev swig

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Create Virtual Environment and install dependencies
uv sync --extra raspberrypi
source .venv/bin/activate

# Install Waveshare Python depedencies
if [ -d TP_lib ]
then
    echo Waveshare Python libraries already downloaded.
else
    rm -rf /tmp/Touch_e-Paper_HAT
    git clone https://github.com/waveshare/Touch_e-Paper_HAT /tmp/Touch_e-Paper_HAT

    # Checkout known working version
    git -C /tmp/Touch_e-Paper_HAT checkout 00b67c802b2e3ce5579236d3ad5e9e8b7c197be1

    cp -r /tmp/Touch_e-Paper_HAT/python/lib/TP_lib TP_lib
    rm -rf /tmp/Touch_e-Paper_HAT
fi

# Install fonts
if [ -f fonts/Roboto-Regular.ttf ]
then
    echo Fonts already downloaded.
else
    mkdir -p fonts
    cd fonts
    ZIP=/tmp/roboto.zip
    wget --output-document=${ZIP} https://github.com/googlefonts/roboto-2/releases/download/v2.138/roboto-android.zip
    unzip ${ZIP} Roboto-Regular.ttf Roboto-Bold.ttf RobotoCondensed-Regular.ttf
    rm ${ZIP}
    cd ..
fi

# Create config file
case "${SOURCE}" in
    1)
        SOURCE=nexbuses
        ;;
    2)
        SOURCE=bustimes
        ;;
    3)
        SOURCE=oxontime
        ;;
esac

cat <<END_OF_CONFIG >config.yml
# The source for the bus times.  One of:
# nextbuses - https://www.nextbuses.mobi
# bustimes - https://bustimes.org
# oxontime - https://oxontime.com (Oxfordshire only, more accurate)
source: ${SOURCE}

# A heartbeat file to update every time the display is updated
# This can be used to monitor the display is still running
heartbeat_file: /tmp/heartbeat

# The version of the Waveshare 2.13inch display
# This will be 2, 3 or 4
display_version: ${DISPLAY_VERSION}

# The list of bus stops to display times for
bus_stop_id:
END_OF_CONFIG

for BUS_STOP in $BUS_STOPS
do
    echo "- ${BUS_STOP}" >>config.yml
done

# Create start up script
cat <<END_OF_SCRIPT >run-nimbus.sh
#!/usr/bin/bash

touch /tmp/heartbeat
cd ${HOME}/nimbus
source .venv/bin/activate
python -m nimbus >nimbus.out 2>&1
END_OF_SCRIPT

chmod +x run-nimbus.sh

# Update crontab
crontab - <<END_OF_CRONTAB
# Start Nimbus at boot
@reboot $PWD/run-nimbus.sh
# Run the watchdog script every minute
* * * * * $PWD/watchdog.sh
END_OF_CRONTAB

# Finished!
echo Set up complete. Reboot system to start Nimbus.
