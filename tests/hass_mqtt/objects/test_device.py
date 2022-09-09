from __future__ import annotations

import pytest

from hass_mqtt import Device, DeviceConfigurationException


def test_valid_configuration() -> None:
    """Ensure that no exception is raised when either identifiers or connections, or both, are configured."""
    Device(name="foo", identifiers="baz")
    Device(name="foo", connections=[("link", "bar")])
    Device(name="foo", identifiers="baz", connections=[("link", "bar")])


def test_invalid_configuration() -> None:
    """Ensure that an exception is raised if neither identifiers nor connections are configured."""
    with pytest.raises(DeviceConfigurationException):
        Device(name="foo")
