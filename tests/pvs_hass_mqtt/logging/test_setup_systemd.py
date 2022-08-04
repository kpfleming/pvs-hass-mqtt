from __future__ import annotations

import logging
from collections.abc import Iterator

import pytest
from attrs import astuple, define
from mock import MagicMock
from pytest_mock import MockerFixture

from pvs_hass_mqtt.cli import SystemdLoggingSetupError, setup_logging


@define(kw_only=True)
class JournalHandlers:
    main: MagicMock
    debug: MagicMock


@pytest.fixture()
def mock_handlers(mocker: MockerFixture) -> Iterator[JournalHandlers]:
    """Mock the 'systemd' package and the JOURNAL_STREAM environment variable."""
    mocked_systemd = mocker.MagicMock()
    handlers = JournalHandlers(main=mocker.MagicMock(), debug=mocker.MagicMock())
    mocked_systemd.journal.JournalHandler.side_effect = astuple(handlers)
    mocker.patch.dict("sys.modules", {"systemd": mocked_systemd})
    mocker.patch.dict("os.environ", {"JOURNAL_STREAM": "set"})
    yield handlers
    # add a no-op as 'teardown', since if 'return' was used
    # the patches would be torn down as the fixture object
    # was returned
    pass


@pytest.mark.logging()
def test_systemd_not_available(mocker: MockerFixture) -> None:
    """Ensure that systemd logging setup fails when systemd package is not available."""
    mocker.patch.dict("sys.modules", {"systemd": None})
    with pytest.raises(SystemdLoggingSetupError) as excinfo:
        setup_logging("systemd", logging.WARNING)
    assert "not installed" in str(excinfo.value)


@pytest.mark.logging()
def test_systemd_not_in_use(mock_handlers: JournalHandlers, mocker: MockerFixture) -> None:
    """Ensure that systemd logging setup fails when systemd is not in use."""
    mocker.patch.dict("os.environ", clear=True)
    with pytest.raises(SystemdLoggingSetupError) as excinfo:
        setup_logging("systemd", logging.WARNING)
    assert "not running" in str(excinfo.value)


@pytest.mark.logging()
def test_systemd_set_level(mock_handlers: JournalHandlers) -> None:
    """Ensure that the specified level is passed to the JournalHandler."""
    setup_logging("systemd", logging.INFO)
    mock_handlers.main.setLevel.assert_called_with(logging.INFO)


@pytest.mark.logging()
def test_systemd_main_handler_invoked(mock_handlers: JournalHandlers) -> None:
    """Ensure that a message is passed to the main JournalHandler."""
    setup_logging("systemd", logging.WARNING)
    # inject the level into the main handler
    mock_handlers.main.level = logging.WARNING
    # inject the level into the debug handler
    mock_handlers.debug.level = logging.DEBUG
    logging.getLogger(__name__).warning("TESTwarningTEST")
    mock_handlers.main.handle.assert_called_once()
    mock_handlers.debug.handle.assert_called_once()


@pytest.mark.logging()
def test_systemd_debug_handler_invoked(mock_handlers: JournalHandlers) -> None:
    """Ensure that a message is passed to the debug JournalHandler."""
    setup_logging("systemd", logging.DEBUG)
    # inject the level into the main handler
    mock_handlers.main.level = logging.WARNING
    # inject the level into the debug handler
    mock_handlers.debug.level = logging.DEBUG
    logging.getLogger(__name__).debug("TESTdebugTEST")
    mock_handlers.main.handle.assert_not_called()
    mock_handlers.debug.handle.assert_called_once()


@pytest.mark.logging()
def test_systemd_debug_handler_module_name(mock_handlers: JournalHandlers) -> None:
    """Ensure that messages at the DEBUG level include the module name."""
    setup_logging("systemd", logging.DEBUG)
    mock_handlers.debug.setFormatter.assert_called_once()
    fmt = mock_handlers.debug.setFormatter.call_args.args[0]
    rec = logging.makeLogRecord(
        {
            "name": "TESTnameTEST",
            "msg": "TEST",
        }
    )
    msg = fmt.format(rec)
    assert "TESTnameTEST" in msg
