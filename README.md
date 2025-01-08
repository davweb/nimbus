# nimbus

Display bus arrival times on a Raspberry Pi with an e-ink screen.

The display shows up to three upcoming buses for a stop. Touching the display cycles through different stops.

![Photo of nimbus running](sample.jpeg)

## Hardware
This is inteded for use with:

* A [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
* A [Waveshare 2.13inch Touch e-Paper HAT](https://www.waveshare.com/wiki/2.13inch_Touch_e-Paper_HAT)

The [e-Paper HAT is available with a case from The Pi Hut](https://thepihut.com/products/2-13-touchscreen-e-paper-display-case-for-raspberry-pi-zero).


## Bus Time Data
Nimbus gets it bus time data by scraping one of three websites:

| Website | Option | Notes |
| ------- | ------ | ----- |
| [Nextbuses](https://nextbuses.mobi/) | `nextbuses` | |
| [bustimes.org](https://bustimes.org/) | `bustimes` | |
| [Oxontime](https://oxontime.com/) | `oxontime` | Oxfordshire only |

Select the site you wish you use during set-up.

## Automated Set-Up

Firstly get the IDs of the bus stops you want to display from [here](https://bus.traveluk.info/index.php/stop-finder).  The IDs will be a list of letters and numbers like `340000006R1`.

Image the SD Card for the Raspberry Pi Zero 2 W with *Rasperry Pi OS Lite (64-bit)* using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).  Use the settings in the imager to set hostname, enable SSH and specify the wi-fi password.

One the Pi has booted, login via SSH.  Install `git`and then clone this repository:

```
sudo apt-get install -y git
git clone https://github.com/davweb/nimbus.git
```

Run the set up script.
```
cd nimbus
./setup.sh
```

Enter the required details when prompted.  The script will configure the Raspberry Pi, install the required dependencies, create a configuration file and schedule Nimbus to run using `cron`.

## Options

Nimbus is configured either through a YAML configuration file or command line options.

Look at `sample-config.yml` for the configuration file format or run the following command to see the command line options:

```
python -m nimbus --help
```





