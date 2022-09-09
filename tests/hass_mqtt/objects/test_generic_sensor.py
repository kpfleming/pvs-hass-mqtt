from __future__ import annotations

from hass_mqtt.sensors import GenericSensor


def test_device_class() -> None:
    """Ensure that the proper device class is set."""
    b = GenericSensor(name="foo", value=0)
    assert b.device_class is None
