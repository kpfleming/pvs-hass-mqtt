from __future__ import annotations

from hass_mqtt import SensorDeviceClass, SensorStateClass, UnitOfMeasurement
from hass_mqtt.sensors import CurrentSensor


def test_device_class() -> None:
    """Ensure that the proper device class is set."""
    b = CurrentSensor(name="foo", value=0)
    assert b.device_class == SensorDeviceClass.current


def test_default_state_class() -> None:
    """Ensure that the expected default state class is set when none is provided."""
    b = CurrentSensor(name="foo", value=0)
    assert b.state_class == SensorStateClass.measurement


def test_state_class() -> None:
    """Ensure that a provided state class is set."""
    b = CurrentSensor(name="foo", value=0, state_class=SensorStateClass.total)
    assert b.state_class == SensorStateClass.total


def test_default_unit_of_measurement() -> None:
    """Ensure that the expected default unit of measurement is set when none is provided."""
    b = CurrentSensor(name="foo", value=0)
    assert b.unit_of_measurement == UnitOfMeasurement.current_ampere


def test_unit_of_measurement() -> None:
    """Ensure that a provided unit of measurement is set."""
    b = CurrentSensor(name="foo", value=0, unit_of_measurement=UnitOfMeasurement.current_kiloampere)
    assert b.unit_of_measurement == UnitOfMeasurement.current_kiloampere
