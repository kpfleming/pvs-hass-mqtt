import argparse
import pathlib

from .version import __version__


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Reads data from a SunPower PVS and sends it via MQTT to Home Assistant."
    )
    parser.add_argument(
        "-c",
        "--config-file",
        default="pvs-hass-mqtt.yml",
        type=pathlib.Path,
        help="provide path to configuration file (default: %(default)s)",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        default="/var/lib/pvs-hass-mqtt",
        type=pathlib.Path,
        help="provide path to directory for data storage (default: %(default)s)",
    )
    parser.add_argument(
        "-t", "--test-config", action="store_true", help="test validity of configuration file"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase verbosity of output; specify multiple times to increase further (default: %(default)s)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="display version of this program",
    )
    args = parser.parse_args()

    if not args.config_file.is_file():
        print(f"Path provided to --config-file is not a regular file: {args.config_file}")
        exit(2)

    if not args.data_dir.is_dir():
        print(f"Path provided to --data-dir is not a directory: {args.data_dir}")
        exit(2)
