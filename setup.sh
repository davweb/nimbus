#!/usr/bin/bash

# Install required packages
sudo apt-get install -y gcc python3-dev python3-venv libjpeg-dev

# Create Virtual Environment
if [ -d .venv ]
then
    echo Virtual Environment already exists.
else
    sudo apt-get install -y
    python -m venv --prompt nimbus .venv
fi

# Install standard Python dependencies
source .venv/bin/activate
pip install --upgrade pip pip-tools
pip-sync

# Install Waveshare Python depedencies
if [ -d TP_lib ]
then
    echo Waveshare Python libraries already downloaded.
else
    git clone https://github.com/waveshare/Touch_e-Paper_HAT /tmp/Touch_e-Paper_HAT
    cp -r /tmp/Touch_e-Paper_HAT/python/lib/TP_lib TP_lib
    rm -rf /tmp/Touch_e-Paper_HAT
fi

# Install fonts
if [ -f fonts/Roboto-Regular.ttf ]
then
    echo Fonts already downloaded.
else
    mkdir fonts
    cd fonts
    ZIP=/tmp/roboto.zip
    wget --output-document=${ZIP} https://github.com/googlefonts/roboto-2/releases/download/v2.138/roboto-android.zip
    unzip ${ZIP} Roboto-Regular.ttf Roboto-Bold.ttf RobotoCondensed-Regular.ttf
    rm ${ZIP}
    cd ..
fi
