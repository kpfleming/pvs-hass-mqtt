from __future__ import annotations

from hass_mqtt.binary_sensors import GenericBinarySensor


def test_device_class() -> None:
    """Ensure that the proper device class is set."""
    b = GenericBinarySensor(name="foo", state=False)
    assert b.device_class is None
