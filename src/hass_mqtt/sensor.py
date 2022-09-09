from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Protocol

from attrs import define, field

from .entity import Entity

logger = logging.getLogger(__name__)


class SensorDeviceClass(Enum):
    apparent_power = auto()
    aql = auto()
    battery = auto()
    carbon_dioxide = auto()
    carbon_monoxide = auto()
    current = auto()
    date = auto()
    duration = auto()
    energy = auto()
    frequency = auto()
    gas = auto()
    humidity = auto()
    illuminance = auto()
    monetary = auto()
    nitrogen_dioxide = auto()
    nitrogen_monoxide = auto()
    nitrous_oxide = auto()
    ozone = auto()
    pm1 = auto()
    pm10 = auto()
    pm25 = auto()
    power_factor = auto()
    power = auto()
    pressure = auto()
    reactive_power = auto()
    signal_strength = auto()
    sulphur_dioxide = auto()
    temperature = auto()
    timestamp = auto()
    volatile_organic_compounds = auto()
    voltage = auto()


class SensorStateClass(Enum):
    measurement = auto()
    total = auto()
    total_increasing = auto()


class UnitOfMeasurement(Enum):
    temperature_celsius = "C"
    temperature_fahrenheit = "F"
    power_watt = "W"
    power_kilowatt = "kW"
    voltage = "V"
    energy_watt_hour = "Wh"
    energy_kilowatt_hour = "kWh"
    current_ampere = "A"
    power_volt_ampere = "VA"


@define(kw_only=True)
class Sensor(Entity, Protocol):
    device_class: SensorDeviceClass | None = field(init=False)
    state_class: SensorStateClass | None = None
    unit_of_measurement: UnitOfMeasurement | None = None
