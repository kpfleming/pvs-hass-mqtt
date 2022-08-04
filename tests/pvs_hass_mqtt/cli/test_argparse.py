from __future__ import annotations

import pytest

from pvs_hass_mqtt.cli import parse_args


def test_invalid_arg() -> None:
    """Ensure that an invalid argument is not accepted."""
    with pytest.raises(SystemExit):
        parse_args(["--test-invalid-arg"])


@pytest.mark.parametrize(
    "args",
    [
        ["--config-file", "file"],
        ["-c", "file"],
        ["--data-dir", "dir"],
        ["-d", "dir"],
        ["--log", "console"],
        ["--log", "systemd"],
        ["-l", "console"],
        ["-l", "systemd"],
        ["--test-config"],
        ["-t"],
        ["--verbose"],
        ["-v"],
    ],
)
def test_args(args: list[str]) -> None:
    """Ensure that known arguments are accepted."""
    parse_args(args)


def test_version() -> None:
    """Ensure that '--version' argument is accepted and program exits without an error."""
    with pytest.raises(SystemExit) as excinfo:
        parse_args(["--version"])
    assert excinfo.value.code == 0


def test_multiple_verbose() -> None:
    """Ensure that multiple '--verbose' arguments are accepted."""
    parse_args(["--verbose", "--verbose", "--verbose"])


@pytest.mark.xfail()
@pytest.mark.parametrize(
    "args",
    [
        ["--config-file", "file", "--config-file", "file"],
        ["--data-dir", "dir", "--data-dir", "dir"],
        ["--log", "console", "--log", "systemd"],
    ],
)
def test_duplicate_args(args: list[str]) -> None:
    """Ensure that duplicate args are not accepted."""
    parse_args(args)
