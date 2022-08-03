from __future__ import annotations

import pytest

from pvs_hass_mqtt.cli import parse_args


def test_invalid_arg() -> None:
    """Ensure that an invalid argument is not accepted."""
    with pytest.raises(SystemExit):
        parse_args(["--test-invalid-arg"])
