from __future__ import annotations

from hass_mqtt import SensorDeviceClass
from hass_mqtt.sensors import TemperatureSensor


def test_device_class() -> None:
    """Ensure that the proper device class is set."""
    b = TemperatureSensor(name="foo", value=0)
    assert b.device_class == SensorDeviceClass.temperature
