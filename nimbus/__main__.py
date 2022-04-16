"""Display bus times on an e-ink screen"""

from nimbus import nextbus

def main():
    """Entrypoint function"""

    #bus_stop_id = 'oxfadgpm'
    bus_stop_id = 'oxfadgdw'
    (refresh_time, buses) = nextbus.extract_bus_information(bus_stop_id)

    print(refresh_time)

    for bus in buses:
        print(bus)

if __name__ == '__main__':
    main()
