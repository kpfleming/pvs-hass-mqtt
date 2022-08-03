from __future__ import annotations

import logging
from collections.abc import Iterator

import pytest
from mock import MagicMock
from pytest_mock import MockerFixture

from pvs_hass_mqtt.cli import setup_logging

mocked_systemd = MagicMock()


@pytest.fixture()
def mock_systemd(mocker: MockerFixture) -> Iterator[MagicMock]:
    """Mock the 'systemd' package and the JOURNAL_STREAM environment variable."""
    mocker.patch.dict("sys.modules", {"systemd": mocked_systemd})
    mocker.patch.dict("os.environ", {"JOURNAL_STREAM": "set"})
    yield mocked_systemd
    # add a no-op as 'teardown', since if 'return' was used
    # the patches would be torn down before the fixture object
    # was returned
    pass


@pytest.mark.logging()
def test_systemd_not_available(mocker: MockerFixture, capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that systemd logging setup fails when systemd package is not available."""
    mocker.patch.dict("sys.modules", {"systemd": None})
    with pytest.raises(SystemExit):
        setup_logging("systemd", logging.WARNING)
    captured = capsys.readouterr()
    assert "not installed" in captured.err


@pytest.mark.logging()
def test_systemd_not_in_use(
    mock_systemd: MagicMock, capsys: pytest.CaptureFixture[str], mocker: MockerFixture
) -> None:
    """Ensure that systemd logging setup fails when systemd is not in use."""
    mocker.patch.dict("os.environ", clear=True)
    with pytest.raises(SystemExit):
        setup_logging("systemd", logging.WARNING)
    captured = capsys.readouterr()
    assert "not running" in captured.err


@pytest.mark.logging()
def test_systemd_set_level(mock_systemd: MagicMock, mocker: MockerFixture) -> None:
    """Ensure that the specified level is passed to the JournalHandler."""
    setup_logging("systemd", logging.INFO)
    mock_systemd.journal.JournalHandler().setLevel.assert_called_once_with(logging.INFO)
