import argparse
import logging
import os
import pathlib
import sys

from . import VERSION

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
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
        "-l",
        "--log",
        default="console",
        choices=("console", "systemd"),
        help="specify the destination for logging output (default: %(default)s)",
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
        version="%(prog)s " + VERSION,
        help="display version of this program",
    )

    return parser.parse_args()


def setup_logging(dest: str, level: int) -> None:
    root_logger = logging.root
    root_logger.setLevel(level)

    if dest == "systemd":
        try:
            import systemd  # type: ignore
        except ImportError:
            logger.error("'systemd' logging requested but not installed")
            exit(2)

        if "JOURNAL_STREAM" not in os.environ:
            logger.error("'systemd' logging requested but not running under systemd")
            exit(2)

        journal_handler = systemd.journal.JournalHandler()
        journal_handler.setLevel(level)
        root_logger.addHandler(journal_handler)

    elif dest == "console":
        debug_handler = logging.StreamHandler(stream=sys.stdout)
        debug_handler.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.setLevel(level)
        stderr_handler = logging.StreamHandler(stream=sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        stdout_handler.setFormatter(formatter)
        stderr_handler.setFormatter(formatter)
        # include more details in debug output
        debug_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s: %(message)s")
        debug_handler.setFormatter(debug_formatter)
        # only allow INFO records to stdout
        stdout_handler.addFilter(lambda r: r.levelno == logging.INFO)
        # only allow DEBUG records to debug
        debug_handler.addFilter(lambda r: r.levelno == logging.DEBUG)
        root_logger.addHandler(debug_handler)
        root_logger.addHandler(stdout_handler)
        root_logger.addHandler(stderr_handler)


def cli() -> None:
    args = parse_args()

    if args.verbose >= 2:
        loglevel = logging.DEBUG
    elif args.verbose == 1:
        loglevel = logging.INFO
    else:
        loglevel = logging.WARN

    setup_logging(args.log, loglevel)

    print(os.path.basename(sys.argv[0]) + " - version: " + VERSION)

    if not args.config_file.is_file():
        logger.error("Path provided to --config-file is not a regular file: %s", args.config_file)
        exit(2)

    if not args.data_dir.is_dir():
        logger.error("Path provided to --data-dir is not a directory: %s", args.data_dir)
        exit(2)
