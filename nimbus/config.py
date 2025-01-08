
"""Merge deskbot configuration from the command line and config files"""

import argparse
from pathlib import Path
import sys
import yaml


def _get_arguments(default_config_file):
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(prog='nimbus', description='Display bus times on an e-ink screen.')
    parser.add_argument('-f', '--config-file', help='Path to the config file', default=default_config_file)
    parser.add_argument('-c', '--console', action='store_true',
                        help='Display output on the console')
    parser.add_argument('-b', '--heartbeat_file', action='store',
                        help='File to touch on every update')
    parser.add_argument('-s', '--source', choices=['nextbuses', 'oxontime', 'bustimes'], action='store',
                        help='Source of bus time data')
    parser.add_argument('-d', '--display_version', choices=['2', '3', '4'], action='store',
                        help='Version of the e-ink display')
    parser.add_argument('bus_stop_id', nargs='*', help='Bus Stop ID')

    return parser.parse_args()


def _parse_config(config_file):
    """Parse the YAML config file"""

    try:
        with open(config_file, 'r', encoding='UTF-8') as stream:
            try:
                return yaml.load(stream, Loader=yaml.BaseLoader)
            except yaml.YAMLError as exc:
                print(f'An error occurred while parsing the YAML file: {exc}', file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        return {}


class Config:
    """Configuration class"""

    def __init__(self):
        self._args = _get_arguments(default_config_file=self.base_dir / 'config.yml')
        self._config_file_name = self._args.config_file
        self._file = _parse_config(self.config_file)

    @property
    def config_file(self):
        """Return the path to the config file"""
        return self._config_file_name

    @property
    def request_timeout(self):
        """Return the HTTP request timeout"""
        return 60

    @property
    def base_dir(self):
        """Return the base directory of the script"""
        return Path(__file__).parent.parent

    @property
    def console(self):
        """Console flag is only from the command line"""
        return self._args.console

    @property
    def source(self):
        """Data source is from the command line or the config file or nextbus by default"""

        if self._args.source:
            return self._args.source

        return self._file.get('source', 'bustimes')

    @property
    def bus_stops(self):
        """Bus Stops is from the command line or the config file or else None"""

        if self._args.bus_stop_id:
            return self._args.bus_stop_id

        return self._file.get('bus_stop_id')

    @property
    def heartbeat_file(self):
        """Heartbeat file path is from the command line or the config file or else None"""

        if self._args.heartbeat_file:
            return self._args.heartbeat_file

        return self._file.get('heartbeat_file')

    @property
    def display_version(self):
        """Display version is from the command line or the config file or else 2"""

        if self._args.display_version:
            return self._args.display_version

        return self._file.get('display_version', '2')


CONFIG = Config()
