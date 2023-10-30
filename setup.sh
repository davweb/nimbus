#!/usr/bin/bash

# Install required packages
sudo apt-get install -y gcc python3-dev python3-venv

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
pip install pip-tools
pip-compile
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
if [ -d fonts ]
then
    echo Fonts already downloaded.
else
    mkdir fonts
    cd fonts

    for FONT in Roboto Roboto+Condensed
    do
        ZIP=/tmp/${FONT}.zip
        wget --output-document=${ZIP} https://fonts.google.com/download?family=${FONT}
        unzip ${ZIP} "*.ttf"
        rm ${ZIP}
    done

    cd ..
fi
