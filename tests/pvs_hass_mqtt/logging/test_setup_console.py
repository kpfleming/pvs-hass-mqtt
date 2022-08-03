from __future__ import annotations

import logging

import pytest

from pvs_hass_mqtt.cli import setup_logging


@pytest.mark.logging()
def test_level_suppression(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that messages below the desired level are suppressed."""
    setup_logging("console", logging.WARNING)
    logging.getLogger(__name__).debug("debug")
    captured = capsys.readouterr()
    assert len(captured.out) == 0
    assert len(captured.err) == 0


@pytest.mark.logging()
def test_level_inclusion(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that messages at the desired level are included."""
    setup_logging("console", logging.WARNING)
    logging.getLogger(__name__).warning("TESTwarningTEST")
    captured = capsys.readouterr()
    assert len(captured.out) == 0
    assert "TESTwarningTEST" in captured.err


@pytest.mark.logging()
def test_info_stdout_only(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that messages at the INFO level appear only on stdout."""
    setup_logging("console", logging.INFO)
    logging.getLogger(__name__).info("TESTinfoTEST")
    captured = capsys.readouterr()
    assert "TESTinfoTEST" in captured.out
    assert len(captured.err) == 0


@pytest.mark.logging()
def test_debug_stdout_only(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that messages at the DEBUG level appear only on stdout."""
    setup_logging("console", logging.DEBUG)
    logging.getLogger(__name__).debug("TESTdebugTEST")
    captured = capsys.readouterr()
    assert "TESTdebugTEST" in captured.out
    assert len(captured.err) == 0


@pytest.mark.logging()
def test_debug_module_name(capsys: pytest.CaptureFixture[str]) -> None:
    """Ensure that messages at the DEBUG level include the module name."""
    setup_logging("console", logging.DEBUG)
    logging.getLogger(__name__).debug("TESTdebugTEST")
    captured = capsys.readouterr()
    assert __name__ in captured.out
    assert len(captured.err) == 0
