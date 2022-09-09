from __future__ import annotations

from hass_mqtt import BinarySensorDeviceClass
from hass_mqtt.binary_sensors import RunningBinarySensor


def test_device_class() -> None:
    """Ensure that the proper device class is set."""
    b = RunningBinarySensor(name="foo", state=False)
    assert b.device_class == BinarySensorDeviceClass.running
