from __future__ import annotations

import pytest

from pvs_hass_mqtt.config import Config, ConfigValidationError


def test_minimal_config() -> None:
    """Ensure that a minimal configuration is accepted."""
    Config._from_dict({"pvs": {"first": {"url": "foo"}}})


def test_missing_pvs() -> None:
    """Ensure that a configuration missing the 'pvs' mapping is not accepted."""
    with pytest.raises(ConfigValidationError) as excinfo:
        Config._from_dict({})
    errors = excinfo.value.errors
    assert "pvs" in errors
    assert "required field" in errors["pvs"]


def test_missing_pvs_url() -> None:
    """Ensure that a missing 'url' field in a 'pvs' mapping entry is not accepted."""
    with pytest.raises(ConfigValidationError) as excinfo:
        Config._from_dict({"pvs": {"first": {"poll_interval": 60}}})
    errors = excinfo.value.errors
    assert "pvs" in errors
    assert "url" in errors["pvs"][0]["first"][0]
    assert "required field" in errors["pvs"][0]["first"][0]["url"]


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (15, "min value"),
        ("abc", "integer type"),
    ],
)
def test_invalid_pvs_poll_interval(value: str, error: str) -> None:
    """Ensure that invalid values for the 'poll_interval' field in a 'pvs' mapping entry are not accepted."""
    with pytest.raises(ConfigValidationError) as excinfo:
        Config._from_dict({"pvs": {"first": {"url": "foo", "poll_interval": value}}})
    errors = excinfo.value.errors
    assert "pvs" in errors
    assert "poll_interval" in errors["pvs"][0]["first"][0]
    assert error in errors["pvs"][0]["first"][0]["poll_interval"][0]


def test_multiple_pvs() -> None:
    """Ensure that the 'pvs' mapping can contain multiple objects."""
    Config._from_dict({"pvs": {"first": {"url": "foo"}, "second": {"url": "foo"}}})
